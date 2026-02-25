# core/boxes.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import random
from PIL import Image, ImageDraw
import math
import sys
from pathlib import Path

# 添加项目根目录到系统路径
sys.path.append(str(Path(__file__).parent.parent))

from core.effects import apply_space_warp
from data.error_messages import SHORT_ERROR_CODES  # 改为绝对导入


def draw_boxes(core, img):
    """绘制四种类型的框"""
    h, w = img.shape[:2]

    # 转换为PIL RGBA格式
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb).convert('RGBA')
    draw = ImageDraw.Draw(img_pil)

    # 错误消息列表
    error_messages = SHORT_ERROR_CODES if core.cfg.use_extended_errors else [
        "ERR", "FAIL", "BAD", "HALT", "STOP", "ABORT", "PANIC"
    ]

    # 根据权重确定每种类型的数量
    total_weight = sum(core.cfg.box_type_weights.values())
    num_boxes = random.randint(*core.cfg.box_count)

    boxes = []
    core.boxes_info = []  # 重置

    for _ in range(num_boxes):
        # 随机选择类型
        r = random.random() * total_weight
        cumsum = 0
        box_type = 'plain'
        for t, wgt in core.cfg.box_type_weights.items():
            cumsum += wgt
            if r <= cumsum:
                box_type = t
                break

        # 随机位置和大小
        box_w = random.randint(int(core.cfg.box_size_range[0] * core.scale),
                               int(core.cfg.box_size_range[1] * core.scale))
        box_h = random.randint(int(box_w * 0.6), int(box_w * 0.9))

        x = random.randint(10, max(11, w - box_w - 10))
        y = random.randint(10, max(11, h - box_h - 10))

        box_info = {
            'type': box_type,
            'x': x, 'y': y,
            'w': box_w, 'h': box_h
        }
        boxes.append(box_info)
        core.boxes_info.append(box_info)

    # 颜色配置
    border_color = core.cfg.color_border

    # 先处理特殊效果
    for box in boxes:
        x, y = box['x'], box['y']
        box_w, box_h = box['w'], box['h']
        box_type = box['type']

        if box_type == 'invert':
            region = img_pil.crop((x + 1, y + 1, x + box_w - 1, y + box_h - 1))
            if region.size[0] > 0 and region.size[1] > 0:
                region_np = np.array(region)
                inverted_np = 255 - region_np
                inverted_img = Image.fromarray(inverted_np)
                img_pil.paste(inverted_img, (x + 1, y + 1))

        elif box_type == 'space_warp':
            img_pil = apply_space_warp(core, img_pil, x, y, box_w, box_h)

    # 绘制框内文字
    for box in boxes:
        x, y = box['x'], box['y']
        box_w, box_h = box['w'], box['h']
        box_type = box['type']

        # 绘制浮点数
        if core.cfg.box_float_display:
            float_text = get_random_float(core)
            font = core.get_font(8)
            bbox = draw.textbbox((0, 0), float_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = x + (box_w - text_width) // 2
            text_y = y + (box_h - 8) // 2
            core.draw_text_with_stroke(draw, text_x, text_y, float_text, font, 
                                       core.cfg.color_float, is_error=False)

        # BIOS框绘制标题
        if box_type == 'bios':
            title_h = int(core.cfg.bios_title_bar_height * core.scale)
            title_format = random.choice(core.cfg.bios_title_formats)
            error_code = random.choice(error_messages)

            title_text = f"{title_format}:{error_code}"
            font = core.get_font(10)
            title_x = x + 3
            title_y = y + (title_h - 10) // 2
            core.draw_text_with_stroke(draw, title_x, title_y, title_text, font, 
                                       core.cfg.color_normal_text, is_error=False)

        # 空间错位框标记
        if box_type == 'space_warp':
            mark_font = core.get_font(6)
            core.draw_text_with_stroke(draw, x + 3, y + 3, "~WARP~", mark_font, 
                                      (150, 150, 150, 200), is_error=False)

        core.stats['boxes_drawn'] += 1

    # 绘制框间中点连线
    if core.cfg.box_line_connect_chance > 0:
        img_pil = draw_box_connections(core, img_pil, boxes)

    # 绘制边框
    border_layer = Image.new('RGBA', img_pil.size, (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_layer)

    for box in boxes:
        x, y = box['x'], box['y']
        box_w, box_h = box['w'], box['h']

        border_draw.rectangle(
            [x, y, x + box_w, y + box_h],
            outline=border_color,
            width=core.cfg.box_border_thickness
        )

        if box['type'] == 'bios':
            title_h = int(core.cfg.bios_title_bar_height * core.scale)
            border_draw.line(
                [x, y + title_h, x + box_w, y + title_h],
                fill=border_color,
                width=core.cfg.box_border_thickness
            )

    img_pil = Image.alpha_composite(img_pil, border_layer)

    core.log_debug(f"绘制 {len(boxes)} 个框 (其中空间错位框: {core.stats['warp_boxes']})")

    result = cv2.cvtColor(np.array(img_pil.convert('RGB')), cv2.COLOR_RGB2BGR)
    return result


def draw_box_connections(core, img_pil, boxes):
    """绘制框之间的中点连线"""
    if len(boxes) < 2:
        return img_pil

    # 计算每个框的中点
    centers = []
    for box in boxes:
        cx = box['x'] + box['w'] // 2
        cy = box['y'] + box['h'] // 2
        centers.append((cx, cy, box))

    # 创建连线层
    line_layer = Image.new('RGBA', img_pil.size, (0, 0, 0, 0))
    line_draw = ImageDraw.Draw(line_layer)

    connections = 0
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            dist = math.sqrt((centers[i][0] - centers[j][0])**2 +
                             (centers[i][1] - centers[j][1])**2)

            if dist < core.cfg.box_line_max_distance * core.scale:
                if random.random() < core.cfg.box_line_connect_chance * (1 - dist / (core.cfg.box_line_max_distance * core.scale)):
                    color = core.cfg.box_line_color

                    if random.random() < core.cfg.box_line_jitter_chance:
                        mid_x = (centers[i][0] + centers[j][0]) // 2
                        mid_y = (centers[i][1] + centers[j][1]) // 2
                        jitter_x = mid_x + random.randint(-core.cfg.box_line_jitter_amount,
                                                          core.cfg.box_line_jitter_amount)
                        jitter_y = mid_y + random.randint(-core.cfg.box_line_jitter_amount,
                                                          core.cfg.box_line_jitter_amount)
                        points = [
                            (centers[i][0], centers[i][1]),
                            (jitter_x, jitter_y),
                            (centers[j][0], centers[j][1])
                        ]
                        for k in range(len(points) - 1):
                            line_draw.line([points[k], points[k + 1]],
                                           fill=color, width=core.cfg.box_line_thickness)
                    else:
                        line_draw.line([(centers[i][0], centers[i][1]),
                                        (centers[j][0], centers[j][1])],
                                       fill=color, width=core.cfg.box_line_thickness)

                    connections += 1

    img_pil = Image.alpha_composite(img_pil, line_layer)
    core.stats['box_connections'] = connections
    core.log_debug(f"绘制 {connections} 条框间连线")

    return img_pil


def get_random_float(core):
    """生成随机浮点数"""
    value = random.uniform(*core.cfg.box_float_range)
    return f"{value:.{core.cfg.box_float_precision}f}"