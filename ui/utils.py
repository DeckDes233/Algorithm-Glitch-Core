# ui/utils.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import gradio as gr
import json
import os
from typing import Tuple
from PIL import Image
import numpy as np

from config import CyberConfig


def rgba_to_hex(color: Tuple[int, int, int, int]) -> str:
    """将RGBA颜色转换为十六进制字符串"""
    r, g, b, a = color
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    """将十六进制颜色转换为RGBA整数元组"""
    if not hex_color:
        return (255, 255, 255, 255)

    # 移除 # 前缀
    hex_color = hex_color.lstrip('#')

    try:
        # 处理不同长度的hex
        if len(hex_color) == 6:  # RGB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b, 255)
        elif len(hex_color) == 8:  # RGBA
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
            return (r, g, b, a)
        else:
            # 默认返回白色
            return (255, 255, 255, 255)
    except ValueError:
        # 如果转换失败，返回默认值
        return (255, 255, 255, 255)


def rgba_to_cv_color(color: Tuple[int, int, int, int]) -> Tuple[int, int, int]:
    """将RGBA转换为OpenCV BGR格式"""
    return (color[2], color[1], color[0])


def preview_config(config: CyberConfig) -> str:
    """预览配置信息"""
    preview = """
| 配置项 | 值 |
|--------|-----|
"""

    preview += f"| 错误文字颜色 | {rgba_to_hex(config.color_error_text)} |\n"
    preview += f"| 普通文字颜色 | {rgba_to_hex(config.color_normal_text)} |\n"
    preview += f"| 边框颜色 | {rgba_to_hex(config.color_border)} |\n"
    preview += f"| 框数量范围 | {config.box_count[0]}-{config.box_count[1]} |\n"
    preview += f"| 框大小范围 | {config.box_size_range[0]}-{config.box_size_range[1]} |\n"
    preview += f"| 连线概率 | {config.box_line_connect_chance:.2f} |\n"
    preview += f"| 错位强度 | {config.warp_intensity:.2f} |\n"
    preview += f"| 景深效果 | {'开启' if config.enable_depth_of_field else '关闭'} |\n"
    preview += f"| 扩展错误消息 | {'开启' if config.use_extended_errors else '关闭'} |\n"

    return preview


def save_config(config: CyberConfig, filepath: str):
    """保存配置到JSON文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    config_dict = config.to_dict()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config_dict, f, indent=2, ensure_ascii=False)

    return f"配置已保存到: {filepath}"


def load_config(filepath: str) -> CyberConfig:
    """从JSON文件加载配置"""
    with open(filepath, 'r', encoding='utf-8') as f:
        config_dict = json.load(f)

    return CyberConfig.from_dict(config_dict)


def get_example_images() -> list:
    """获取示例图片列表"""
    examples_dir = "static/examples"
    os.makedirs(examples_dir, exist_ok=True)

    # 如果没有示例图片，创建一个简单的示例
    if not os.listdir(examples_dir):
        create_example_image(os.path.join(examples_dir, "example1.jpg"))
        create_example_image(os.path.join(examples_dir, "example2.jpg"))

    return [os.path.join(examples_dir, f) for f in os.listdir(examples_dir)
            if f.lower().endswith(('.jpg', '.png', '.jpeg'))]


def create_example_image(path: str):
    """创建一个简单的示例图片"""
    img = Image.new('RGB', (800, 600), color='darkgray')
    img.save(path)


def update_config_from_ui(config: CyberConfig, **kwargs) -> CyberConfig:
    """从UI参数更新配置"""
    for key, value in kwargs.items():
        if hasattr(config, key) and value is not None:
            setattr(config, key, value)
    return config