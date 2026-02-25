# core/text.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import random
from PIL import Image, ImageDraw
import sys
from pathlib import Path

# 添加项目根目录到系统路径
sys.path.append(str(Path(__file__).parent.parent))

from data.error_messages import (
    SHORT_ERROR_CODES,
    get_random_short_code,
    format_error_with_hex,
    format_error_with_code
)


def draw_chaotic_text(core, pts):
    """绘制混乱的文字效果"""
    img_pil = Image.fromarray(cv2.cvtColor(core.canvas, cv2.COLOR_BGR2RGB)).convert('RGBA')
    draw = ImageDraw.Draw(img_pil)

    f_tiny = core.get_font(8)
    f_small = core.get_font(10)
    f_med = core.get_font(13)
    f_large = core.get_font(18)

    styles = list(core.cfg.style_weights.keys())
    weights = list(core.cfg.style_weights.values())

    num_blocks = random.randint(*core.cfg.log_blocks_range)
    core.stats['text_blocks'] = num_blocks

    for _ in range(num_blocks):
        style = random.choices(styles, weights=weights, k=1)[0]

        base_x = random.randint(int(10 * core.scale), int(core.w * 0.85))
        curr_y = int(core.h * random.uniform(0.1, 0.9))
        curr_x = base_x

        for i in range(random.randint(*core.cfg.log_lines_per_block)):
            error_msg = core.get_random_error_message()

            is_error = random.random() > 0.7

            tag = random.choice(["[ERR]", "[WARN]", "[FAIL]", "[BUG]", "[FATAL]"]) if is_error else \
                  random.choice(["[INFO]", "[DEBUG]", "[LOG]", "[TRACE]"])

            format_type = random.choice(['plain', 'hex', 'code'])
            if format_type == 'hex':
                full_text = format_error_with_hex(error_msg)
            elif format_type == 'code':
                full_text = format_error_with_code(error_msg, get_random_short_code())
            else:
                full_text = f"{tag} {error_msg}"

            if style == 'staircase':
                step_offset = random.randint(*core.cfg.staircase_step) * core.scale
                curr_x += step_offset
            elif style == 'jitter':
                curr_x = base_x + random.randint(-40, 40) * core.scale
            else:
                curr_x = base_x

            curr_y += int(random.uniform(15, 40) * core.scale)

            if style == 'torn' and random.random() < core.cfg.torn_trigger_chance:
                split_point = len(tag)
                part1 = full_text[:split_point]
                part2 = full_text[split_point:]

                core.draw_text_with_stroke(draw, curr_x, curr_y, part1, f_small,
                                          core.cfg.color_normal_text, is_error=is_error)

                gap_x = random.randint(*core.cfg.torn_offset_x) * core.scale
                gap_y = random.randint(*core.cfg.torn_offset_y) * core.scale

                core.draw_text_with_stroke(draw, curr_x + gap_x, curr_y + gap_y, part2, f_small,
                                          core.cfg.color_normal_text, is_error=is_error)
            else:
                core.draw_text_with_stroke(draw, curr_x, curr_y, full_text, f_small,
                                          core.cfg.color_normal_text, is_error=is_error)

    # 独立报错
    for _ in range(random.randint(*core.cfg.fatal_error_count)):
        ex = random.randint(int(core.w * 0.1), int(core.w * 0.8))
        ey = random.randint(int(core.h * 0.1), int(core.h * 0.8))

        error_msg = core.get_random_error_message()
        hex_addr = f"0x{random.randint(0, 0xFFFFFF):06X}"
        err_msg = erode_text(core, f"{error_msg} at {hex_addr}", 0.1)
        core.draw_text_with_stroke(draw, ex, ey, err_msg, f_med,
                                  core.cfg.color_error_text, is_error=True)

        if pts and random.random() < core.cfg.hud_line_chance:
            target_pt = random.choice(pts)
            draw.line([(ex + 80 * core.scale, ey + 5 * core.scale), target_pt],
                      fill=(200, 200, 200, 60), width=1)

    # 节点文字
    for pt in pts:
        if random.random() > core.cfg.node_text_chance:
            continue
        txt = random.choice(SHORT_ERROR_CODES if core.cfg.use_extended_errors else
                           ["ERR", "FAIL", "BAD", "NULL"])
        ox = random.randint(4, 15) * (1 if random.random() > 0.5 else -1)
        oy = random.randint(4, 15) * (1 if random.random() > 0.5 else -1)
        core.draw_text_with_stroke(draw, pt[0] + ox, pt[1] + oy, txt, f_tiny,
                                  core.cfg.color_normal_text, is_error=False)

    # 标题
    t1 = erode_text(core, "SYSTEM_PANIC", core.cfg.title_erosion_rate)
    t2 = erode_text(core, ":: KERNEL_DUMP", core.cfg.title_erosion_rate * 0.6)
    t3 = erode_text(core, "CRITICAL ERROR", core.cfg.title_erosion_rate * 0.4)

    core.draw_text_with_stroke(draw, 20, 20, t1, f_large,
                              core.cfg.color_normal_text, is_error=True)
    core.draw_text_with_stroke(draw, 25, 20 + 22 * core.scale, t2, f_large,
                              core.cfg.color_normal_text, is_error=False)
    core.draw_text_with_stroke(draw, 20, 20 + 50 * core.scale, t3, f_med,
                              core.cfg.color_error_text, is_error=True)

    result = cv2.cvtColor(np.array(img_pil.convert('RGB')), cv2.COLOR_RGB2BGR)
    return result


def erode_text(core, text, erosion_rate):
    """文字侵蚀效果"""
    return "".join(
        [random.choice(["_", " ", ".", "x"]) if random.random() < erosion_rate and c != " " else c
         for c in text])