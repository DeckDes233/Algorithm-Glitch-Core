# core/effects.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import random
from PIL import Image, ImageFilter, ImageEnhance
import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


def _fade(t):
    """Perlin噪声的缓和曲线 6t^5 - 15t^4 + 10t^3"""
    return t * t * t * (t * (t * 6 - 15) + 10)


def _lerp(a, b, t):
    """线性插值"""
    return a + t * (b - a)


def _grad_2d(hash_val, x, y):
    """二维梯度向量点积"""
    h = hash_val & 3
    if h == 0:
        return x + y
    elif h == 1:
        return -x + y
    elif h == 2:
        return x - y
    else:
        return -x - y


def _generate_permutation(seed):
    """生成Perlin噪声的排列表"""
    rng = np.random.RandomState(seed)
    p = np.arange(256, dtype=int)
    rng.shuffle(p)
    return np.concatenate([p, p])


def _perlin_noise_2d(x, y, perm):
    """计算单个点的二维Perlin噪声值, 返回[-1, 1]"""
    xi = int(np.floor(x)) & 255
    yi = int(np.floor(y)) & 255
    xf = x - np.floor(x)
    yf = y - np.floor(y)

    u = _fade(xf)
    v = _fade(yf)

    aa = perm[perm[xi] + yi]
    ab = perm[perm[xi] + yi + 1]
    ba = perm[perm[xi + 1] + yi]
    bb = perm[perm[xi + 1] + yi + 1]

    x1 = _lerp(_grad_2d(aa, xf, yf), _grad_2d(ba, xf - 1, yf), u)
    x2 = _lerp(_grad_2d(ab, xf, yf - 1), _grad_2d(bb, xf - 1, yf - 1), u)

    return _lerp(x1, x2, v)


def _perlin_noise_2d_array(h, w, scale, octaves, seed):
    """生成二维Perlin噪声数组, 返回[h, w]的float64数组, 范围[-1, 1]"""
    perm = _generate_permutation(seed)

    noise = np.zeros((h, w), dtype=np.float64)
    amplitude = 1.0
    frequency = 1.0
    max_amplitude = 0.0

    for _ in range(octaves):
        # 向量化计算坐标
        xs = np.arange(w, dtype=np.float64) * frequency / scale
        ys = np.arange(h, dtype=np.float64) * frequency / scale
        xv, yv = np.meshgrid(xs, ys)

        # 逐像素计算(用向量化没法完全避免循环, 但numpy广播加速)
        octave_noise = np.zeros((h, w), dtype=np.float64)
        for yi in range(h):
            for xi in range(w):
                octave_noise[yi, xi] = _perlin_noise_2d(xv[yi, xi], yv[yi, xi], perm)

        noise += octave_noise * amplitude
        max_amplitude += amplitude
        amplitude *= 0.5
        frequency *= 2.0

    noise /= max_amplitude
    return noise


def apply_perlin_noise(core, img):
    """应用Perlin噪声 - 模拟胶片颗粒和自然纹理"""
    h, w = img.shape[:2]
    intensity = core.cfg.noise_perlin_intensity * core.cfg.noise_strength

    noise = _perlin_noise_2d_array(
        h, w,
        scale=core.cfg.noise_perlin_scale,
        octaves=core.cfg.noise_perlin_octaves,
        seed=core.seed
    )

    # 将噪声映射到[-intensity, intensity]
    noise_map = (noise * intensity).astype(np.float64)

    # 应用到图像
    result = img.astype(np.float64)
    for c in range(3):
        result[:, :, c] += noise_map

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_rgb_noise(core, img):
    """RGB通道独立噪声 - 三个通道分别添加不同程度噪声"""
    h, w = img.shape[:2]
    strength = core.cfg.noise_strength
    intensities = [
        core.cfg.noise_rgb_r_intensity * strength,
        core.cfg.noise_rgb_g_intensity * strength,
        core.cfg.noise_rgb_b_intensity * strength,
    ]

    result = img.astype(np.float64)
    for c in range(3):
        noise = _perlin_noise_2d_array(
            h, w,
            scale=core.cfg.noise_perlin_scale * 1.2,
            octaves=max(2, core.cfg.noise_perlin_octaves - 1),
            seed=core.seed + c * 100
        )
        result[:, :, c] += noise * intensities[c]

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_scanline_noise(core, img):
    """扫描线噪声 - 模拟老式电视扫描线干扰"""
    h, w = img.shape[:2]
    intensity = core.cfg.noise_scanline_intensity * core.cfg.noise_strength
    freq = core.cfg.noise_scanline_frequency

    result = img.astype(np.float64)

    # 每条扫描线施加随机偏移
    rng = np.random.RandomState(core.seed + 777)
    for y in range(0, h, 2):
        # 扫描线基础亮度调制: 正弦波 + 随机抖动
        sine_val = np.sin(2.0 * np.pi * freq * y / h)
        jitter = rng.uniform(-0.3, 0.3)
        line_intensity = intensity * (0.5 + 0.5 * sine_val + jitter)

        # 偶数行稍微变暗, 模拟CRT扫描线
        if y % 2 == 0:
            result[y, :, :] -= line_intensity * 0.6
        else:
            result[y, :, :] += line_intensity * 0.2

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_crt_effects(core, img):
    """应用CRT屏幕效果"""
    h, w = img.shape[:2]
    b, g, r = cv2.split(img)
    shift_x = int(random.uniform(1, core.cfg.rgb_shift_max) * core.scale)
    shift_y = int(random.uniform(0, 1) * core.scale)

    # 红色通道偏移
    M_r = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    r_shifted = cv2.warpAffine(r, M_r, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 蓝色通道反向偏移
    M_b = np.float32([[1, 0, -shift_x], [0, 1, -shift_y]])
    b_shifted = cv2.warpAffine(b, M_b, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 合并通道
    glitched = cv2.merge((b_shifted, g, r_shifted))

    # 扫描线效果
    scanline_spacing = max(2, int(3 * core.scale))
    for y in range(0, h, scanline_spacing):
        glitched[y:y + 1] = glitched[y:y + 1] * core.cfg.scanline_darkness

    return glitched


def apply_depth_of_field(core, img_pil):
    """应用景深效果"""
    if not core.cfg.enable_depth_of_field:
        return img_pil

    w, h = img_pil.size
    focus_x = int(w * core.cfg.depth_focus_center[0])
    focus_y = int(h * core.cfg.depth_focus_center[1])
    focus_radius = min(w, h) * core.cfg.depth_focus_radius

    # 创建深度蒙版
    depth_mask = Image.new('L', (w, h), 0)

    # 创建径向渐变
    for y in range(h):
        for x in range(w):
            dist = math.sqrt((x - focus_x)**2 + (y - focus_y)**2)
            if dist > focus_radius:
                fade = min(1.0, (dist - focus_radius) / (min(w, h) * core.cfg.depth_fade_start))
                depth = int(255 * fade)
                depth_mask.putpixel((x, y), depth)

    # 应用模糊效果
    blurred = img_pil.filter(ImageFilter.GaussianBlur(radius=core.cfg.depth_blur_amount))
    enhancer = ImageEnhance.Brightness(blurred)
    darkened = enhancer.enhance(1.0 - core.cfg.depth_darken_amount * 0.3)

    # 根据深度蒙版混合
    result = Image.composite(darkened, img_pil, depth_mask)
    return result


def apply_space_warp(core, img_pil, x, y, w, h):
    """应用空间错位效果"""
    # 裁剪区域
    region = img_pil.crop((x, y, x + w, y + h))
    if region.size[0] == 0 or region.size[1] == 0:
        return img_pil

    region_np = np.array(region)
    h_reg, w_reg = region_np.shape[:2]

    # 创建扭曲后的图像
    warped_np = region_np.copy()

    # 根据强度决定错位程度
    intensity = core.cfg.warp_intensity * random.uniform(0.8, 1.2)
    segments = max(2, int(core.cfg.warp_segments * intensity))

    # 分段错位
    if random.random() < 0.7:
        segment_height = h_reg // segments
        for i in range(segments):
            y_start = i * segment_height
            y_end = (i + 1) * segment_height if i < segments - 1 else h_reg

            if random.random() < core.cfg.warp_glitch_chance:
                shift = int(random.randint(*core.cfg.warp_shift_range) * intensity * core.scale)

                if random.random() > 0.5:
                    warped_np[y_start:y_end, shift:w_reg] = region_np[y_start:y_end, :w_reg-shift]
                    warped_np[y_start:y_end, :shift] = region_np[y_start:y_end, w_reg-shift:]
                else:
                    warped_np[y_start:y_end, :w_reg-shift] = region_np[y_start:y_end, shift:]
                    warped_np[y_start:y_end, w_reg-shift:] = region_np[y_start:y_end, :shift]

    # 颜色通道错位
    if core.cfg.warp_color_shift and random.random() < 0.5:
        r_channel = warped_np[:, :, 0].copy()
        g_channel = warped_np[:, :, 1].copy()
        b_channel = warped_np[:, :, 2].copy()

        r_shift = int(random.randint(-5, 5) * intensity)
        g_shift = int(random.randint(-5, 5) * intensity)
        b_shift = int(random.randint(-5, 5) * intensity)

        if r_shift != 0:
            r_channel = np.roll(r_channel, r_shift, axis=1)
        if g_shift != 0:
            g_channel = np.roll(g_channel, g_shift, axis=1)
        if b_shift != 0:
            b_channel = np.roll(b_channel, b_shift, axis=1)

        warped_np = np.stack([r_channel, g_channel, b_channel], axis=2)

    # 扫描线抖动
    if core.cfg.warp_scanline_jitter and random.random() < 0.4:
        for line in range(0, h_reg, 2):
            if random.random() < 0.3:
                line_shift = int(random.randint(-3, 3) * intensity)
                if line_shift != 0:
                    warped_np[line:line+1] = np.roll(warped_np[line:line+1], line_shift, axis=1)

    # 像素化效果
    if random.random() < 0.2:
        pixel_size = max(2, int(4 * intensity))
        small = cv2.resize(warped_np, (w_reg // pixel_size, h_reg // pixel_size),
                           interpolation=cv2.INTER_LINEAR)
        warped_np = cv2.resize(small, (w_reg, h_reg), interpolation=cv2.INTER_NEAREST)

    # 转换回PIL并粘贴
    warped_img = Image.fromarray(warped_np)
    img_pil.paste(warped_img, (x, y))

    return img_pil