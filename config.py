# config.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Tuple, Dict, List, Any
import json


def ensure_rgba(color) -> Tuple[int, int, int, int]:
    """确保颜色值是RGBA格式的整数元组"""
    if isinstance(color, str):
        # 处理十六进制字符串
        color = color.lstrip('#')
        if len(color) == 6:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            return (r, g, b, 255)
        elif len(color) == 8:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            a = int(color[6:8], 16)
            return (r, g, b, a)
    elif isinstance(color, (list, tuple)):
        # 确保所有值都是整数
        return tuple(int(x) for x in color)
    return (255, 255, 255, 255)  # 默认白色


@dataclass
class CyberConfig:
    """赛博朋克风格配置类"""

    # 1. 颜色设定 - 使用 ensure_rgba 确保格式正确
    color_warning: Tuple[int, int, int, int] = (255, 50, 50, 255)
    color_error_text: Tuple[int, int, int, int] = (255, 50, 50, 255)
    color_normal_text: Tuple[int, int, int, int] = (255, 255, 255, 255)
    color_border: Tuple[int, int, int, int] = (255, 255, 255, 255)
    color_line: Tuple[int, int, int, int] = (255, 255, 255, 180)
    color_float: Tuple[int, int, int, int] = (255, 255, 255, 255)
    mesh_color: Tuple[int, int, int, int] = (255, 255, 255, 200)

    # 2. 网格与线条
    mesh_complexity: int = 220
    line_connect_chance: float = 0.18
    nerve_mutation_chance: float = 0.25

    # 3. 文本散布
    log_blocks_range: Tuple[int, int] = (4, 28)
    log_lines_per_block: Tuple[int, int] = (2, 3)
    node_text_chance: float = 0.35
    hex_dump_areas: int = 8

    # 4. 故障与侵蚀
    title_erosion_rate: float = 0.33
    fatal_error_count: Tuple[int, int] = (4, 6)
    hud_line_chance: float = 0.6

    # 5. CRT 屏幕特效
    rgb_shift_max: float = 3.0
    scanline_darkness: float = 0.88

    # 6. 排版崩坏风格控制
    style_weights: Dict[str, int] = field(default_factory=lambda: {
        'staircase': 4,
        'torn': 5,
        'jitter': 2,
        'normal': 1
    })

    torn_trigger_chance: float = 0.6
    torn_offset_x: Tuple[int, int] = (60, 150)
    torn_offset_y: Tuple[int, int] = (-10, 20)
    staircase_step: Tuple[int, int] = (10, 30)

    # 7. 框配置
    box_count: Tuple[int, int] = (18, 30)
    box_size_range: Tuple[int, int] = (40, 150)
    box_border_thickness: int = 1
    box_line_connect_chance: float = 1.0
    box_line_max_distance: float = 300
    box_line_thickness: int = 1
    box_line_color: Tuple[int, int, int, int] = (255, 255, 255, 180)
    box_line_jitter_chance: float = 0.3
    box_line_jitter_amount: int = 15
    box_float_display: bool = True
    box_float_range: Tuple[float, float] = (-999.999, 999.999)
    box_float_precision: int = 3

    box_type_weights: Dict[str, int] = field(default_factory=lambda: {
        'plain': 3,
        'invert': 2,
        'bios': 4,
        'space_warp': 3
    })

    # BIOS框设置
    bios_title_bar_height: int = 16
    bios_title_formats: List[str] = field(default_factory=lambda: [
        "[BIOS]", "[SETUP]", "[POST]", "[CMOS]", "[ROM]",
        "[ERR]", "[WARN]", "[INFO]", "[FATAL]", "[PANIC]"
    ])

    invert_chance: float = 1.0

    # 8. 空间错位框设置
    warp_intensity: float = 0.7
    warp_segments: int = 10
    warp_glitch_chance: float = 0.8
    warp_shift_range: Tuple[int, int] = (5, 20)
    warp_color_shift: bool = True
    warp_scanline_jitter: bool = True

    # 9. 错误消息配置
    use_extended_errors: bool = True
    error_categories: List[str] = field(default_factory=lambda: [
        'fatal', 'hash', 'key', 'auth', 'network',
        'hardware', 'filesystem', 'database', 'security',
        'crypto', 'runtime', 'driver', 'monitoring', 'ml', 'stack'
    ])

    error_weights: Dict[str, int] = field(default_factory=lambda: {
        'fatal': 1, 'hash': 1, 'key': 1, 'auth': 1, 'network': 1,
        'hardware': 1, 'filesystem': 1, 'database': 1, 'security': 1,
        'crypto': 1, 'runtime': 1, 'driver': 1, 'monitoring': 1,
        'ml': 2, 'stack': 2
    })

    # 10. 景深效果
    enable_depth_of_field: bool = True
    depth_focus_center: Tuple[float, float] = (0.5, 0.5)
    depth_focus_radius: float = 0.3
    depth_blur_amount: float = 1.5
    depth_darken_amount: float = 0.7
    depth_fade_start: float = 0.2

    def __post_init__(self):
        """初始化后处理，确保颜色格式正确"""
        # 确保所有颜色都是正确的RGBA元组
        self.color_warning = ensure_rgba(self.color_warning)
        self.color_error_text = ensure_rgba(self.color_error_text)
        self.color_normal_text = ensure_rgba(self.color_normal_text)
        self.color_border = ensure_rgba(self.color_border)
        self.color_line = ensure_rgba(self.color_line)
        self.color_float = ensure_rgba(self.color_float)
        self.mesh_color = ensure_rgba(self.mesh_color)
        self.box_line_color = ensure_rgba(self.box_line_color)

    def to_dict(self) -> dict:
        """转换为可序列化的字典"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, tuple):
                # 将元组转换为列表以便JSON序列化
                result[key] = list(value)
            elif isinstance(value, (dict, list, int, float, str, bool, type(None))):
                result[key] = value
            elif not key.startswith('_'):
                result[key] = str(value)
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'CyberConfig':
        """从字典创建配置"""
        # 转换列表回元组
        tuple_keys = [
            'color_warning', 'color_error_text', 'color_normal_text', 'color_border',
            'color_line', 'color_float', 'mesh_color', 'box_line_color',
            'torn_offset_x', 'torn_offset_y', 'staircase_step',
            'log_blocks_range', 'log_lines_per_block', 'fatal_error_count',
            'box_count', 'box_size_range', 'box_float_range', 'depth_focus_center',
            'warp_shift_range'
        ]

        for key in tuple_keys:
            if key in data and isinstance(data[key], list):
                data[key] = tuple(data[key])

        # 创建实例
        instance = cls(**data)
        return instance