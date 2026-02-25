# core/renderer.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import random
import os
from PIL import Image, ImageFont, ImageDraw
import time
import math

from config import CyberConfig
from core.effects import apply_crt_effects, apply_depth_of_field
from core.boxes import draw_boxes
from core.text import draw_chaotic_text
from core.utils import detect_subject, draw_sparse_wireframe
from data.error_messages import get_random_error, SHORT_ERROR_CODES


class ConfigurableCyberCore:
    """赛博朋克风格渲染核心"""

    def __init__(self, img_path, font_path, config: CyberConfig, seed=42, debug_mode=False):
        self.seed = seed
        self.font_path = font_path
        self.cfg = config
        self.debug_mode = debug_mode

        self.origin = cv2.imread(img_path)
        if self.origin is None:
            raise ValueError(f"无法读取图片: {img_path}")

        self.h, self.w = self.origin.shape[:2]
        self.scale = self.w / 1200.0
        self.canvas = self.origin.copy()

        random.seed(seed)
        np.random.seed(seed)

        # 安全地转换颜色顺序从RGBA到BGR，确保是整数
        def safe_int(x):
            try:
                return int(x)
            except (ValueError, TypeError):
                return 255  # 默认值

        # 转换颜色，确保所有值都是整数
        self.cv_red = (
            safe_int(self.cfg.color_warning[2]),
            safe_int(self.cfg.color_warning[1]),
            safe_int(self.cfg.color_warning[0])
        )
        self.cv_white = (
            safe_int(self.cfg.color_normal_text[2]),
            safe_int(self.cfg.color_normal_text[1]),
            safe_int(self.cfg.color_normal_text[0])
        )
        self.cv_mesh = (
            safe_int(self.cfg.mesh_color[2]),
            safe_int(self.cfg.mesh_color[1]),
            safe_int(self.cfg.mesh_color[0])
        )

        # 统计信息
        self.stats = {
            'boxes_drawn': 0,
            'text_blocks': 0,
            'errors_used': [],
            'processing_time': 0,
            'box_connections': 0,
            'warp_boxes': 0
        }

        # 存储框的位置信息用于连线
        self.boxes_info = []

    def log_debug(self, message):
        """调试日志"""
        if self.debug_mode:
            print(f"[DEBUG] {message}")

    def get_font(self, size_pt):
        """获取字体"""
        if not self.font_path or not os.path.exists(self.font_path):
            return ImageFont.load_default()
        try:
            # 根据图像缩放调整字体大小
            font_size = int(size_pt * self.scale)
            return ImageFont.truetype(self.font_path, font_size)
        except Exception as e:
            if self.debug_mode:
                print(f"[DEBUG] 字体加载失败: {e}")
            return ImageFont.load_default()

    def draw_text_with_stroke(self, draw, x, y, text, font, fill_color, is_error=False):
        """绘制文字，带黑色描边"""
        stroke_color = (0, 0, 0, 255)

        # 确保坐标是整数
        x = int(x)
        y = int(y)

        # 黑色描边
        draw.text((x - 1, y), text, font=font, fill=stroke_color)
        draw.text((x + 1, y), text, font=font, fill=stroke_color)
        draw.text((x, y - 1), text, font=font, fill=stroke_color)
        draw.text((x, y + 1), text, font=font, fill=stroke_color)

        # 主文字
        if is_error:
            text_color = self.cfg.color_error_text
        else:
            text_color = fill_color
        draw.text((x, y), text, font=font, fill=text_color)

    def get_random_error_message(self):
        """获取随机错误消息"""
        if self.cfg.use_extended_errors:
            categories = list(self.cfg.error_weights.keys())
            weights = list(self.cfg.error_weights.values())
            category = random.choices(categories, weights=weights, k=1)[0]
            self.stats['errors_used'].append(category)
            return get_random_error(category)
        else:
            simple_errors = [
                "KERNEL_PANIC", "SYSTEM_HALT", "MEMORY_CORRUPTION",
                "HASH_MISMATCH", "KEY_EXPIRED", "ACCESS_DENIED",
                "DISK_ERR", "CPU_FAULT", "NETWORK_TIMEOUT"
            ]
            return random.choice(simple_errors)

    def run(self, save_path):
        """运行完整渲染流程"""
        start_time = time.time()

        self.log_debug("开始处理图像...")

        # 保存原始图像的副本
        original = self.canvas.copy()

        hull, mask = detect_subject(self.origin, self.cfg)
        self.log_debug(f"检测到主体，轮廓点数: {len(hull) if hull is not None else 0}")

        pts = draw_sparse_wireframe(self, hull, mask)
        self.log_debug(f"绘制网格，生成 {len(pts)} 个特征点")

        # 绘制文字
        self.canvas = draw_chaotic_text(self, pts)

        # 添加四种类型的框
        self.canvas = draw_boxes(self, self.canvas)

        # 应用景深效果
        if self.cfg.enable_depth_of_field:
            img_pil = Image.fromarray(cv2.cvtColor(self.canvas, cv2.COLOR_BGR2RGB))
            img_pil = apply_depth_of_field(self, img_pil)
            self.canvas = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # 应用CRT效果
        self.canvas = apply_crt_effects(self, self.canvas)

        # 确保图像不是全白
        if np.mean(self.canvas) > 250:
            self.log_debug("警告：检测到图像可能全白，使用原始图像")
            self.canvas = original

        cv2.imwrite(save_path, self.canvas)

        elapsed_time = time.time() - start_time
        self.stats['processing_time'] = elapsed_time

        print(f"Saved: {save_path}")
        if self.debug_mode:
            print(f"[DEBUG] 统计信息: {self.stats}")

    def get_stats(self):
        """获取处理统计信息"""
        return self.stats