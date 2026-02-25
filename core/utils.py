# core/utils.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import random
import os
from PIL import ImageFont


def get_font(core, size_pt):
    """获取字体（备用函数）"""
    if not core.font_path or not os.path.exists(core.font_path):
        return ImageFont.load_default()
    try:
        return ImageFont.truetype(core.font_path, int(size_pt * core.scale))
    except:
        return ImageFont.load_default()


def draw_text_with_stroke(core, draw, x, y, text, font, fill_color, is_error=False):
    """绘制文字，带黑色描边（备用函数）"""
    stroke_color = (0, 0, 0, 255)

    # 黑色描边
    draw.text((x - 1, y), text, font=font, fill=stroke_color)
    draw.text((x + 1, y), text, font=font, fill=stroke_color)
    draw.text((x, y - 1), text, font=font, fill=stroke_color)
    draw.text((x, y + 1), text, font=font, fill=stroke_color)

    # 主文字
    if is_error:
        text_color = core.cfg.color_error_text
    else:
        text_color = fill_color
    draw.text((x, y), text, font=font, fill=text_color)


def detect_subject(img, cfg):
    """检测图像中的主体

    Args:
        img: OpenCV图像 (BGR格式)
        cfg: CyberConfig配置对象

    Returns:
        hull: 凸包轮廓点
        mask: 主体掩码
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 40, 120)
    dilated = cv2.dilate(edges, np.ones((9, 9), np.uint8), iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None

    # 按面积排序，取最大的几个轮廓
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
    all_pts = np.concatenate(contours)
    hull = cv2.convexHull(all_pts)
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [hull], -1, 255, -1)

    return hull, mask


def draw_sparse_wireframe(core, hull, mask):
    """绘制稀疏线框

    Args:
        core: ConfigurableCyberCore实例
        hull: 凸包轮廓点
        mask: 主体掩码

    Returns:
        valid_pts: 有效特征点列表
    """
    if hull is None:
        return []

    gray = cv2.cvtColor(core.origin, cv2.COLOR_BGR2GRAY)

    # 检测特征点
    features = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=int(core.cfg.mesh_complexity * core.scale),
        qualityLevel=0.015,
        minDistance=int(25 * core.scale),
        mask=mask
    )

    points = [tuple(p[0]) for p in features] if features is not None else []

    # 添加轮廓点
    for p in hull:
        points.append(tuple(p[0]))

    # 创建Delaunay三角剖分
    rect = (0, 0, core.w, core.h)
    subdiv = cv2.Subdiv2D(rect)
    valid_pts = []

    for p in points:
        if 0 <= p[0] < core.w and 0 <= p[1] < core.h:
            try:
                subdiv.insert(p)
                valid_pts.append(p)
            except:
                pass

    # 获取三角形并绘制
    triangles = subdiv.getTriangleList()
    overlay = core.canvas.copy()

    for t in triangles:
        pt1, pt2, pt3 = (int(t[0]), int(t[1])), (int(t[2]), int(t[3])), (int(t[4]), int(t[5]))
        cx, cy = (pt1[0] + pt2[0] + pt3[0]) // 3, (pt1[1] + pt2[1] + pt3[1]) // 3

        # 检查中心点是否在主体内
        if cv2.pointPolygonTest(hull, (cx, cy), False) < 0:
            continue

        if random.random() < core.cfg.line_connect_chance:
            draw_nerve_line(core, overlay, pt1, pt2, 1)
            if random.random() > 0.6:
                draw_nerve_line(core, overlay, pt2, pt3, 1)

        if random.random() > 0.95:
            size = int(3 * core.scale)
            cv2.line(overlay, (pt1[0] - size, pt1[1]), (pt1[0] + size, pt1[1]), core.cv_mesh, 1)
            cv2.line(overlay, (pt1[0], pt1[1] - size), (pt1[0], pt1[1] + size), core.cv_mesh, 1)

    cv2.addWeighted(overlay, 0.65, core.canvas, 0.35, 0, core.canvas)
    return valid_pts


def draw_nerve_line(core, img, pt1, pt2, thickness):
    """绘制神经线

    Args:
        core: ConfigurableCyberCore实例
        img: 要绘制的图像
        pt1: 起点
        pt2: 终点
        thickness: 线宽
    """
    # 确保颜色值是整数元组
    color = core.cv_mesh

    # 确保颜色值是三个整数的元组
    if not isinstance(color, tuple) or len(color) != 3:
        color = (255, 255, 255)  # 默认白色

    # 确保所有值都是整数
    color = (int(color[0]), int(color[1]), int(color[2]))

    if random.random() < core.cfg.nerve_mutation_chance:
        mid_x, mid_y = (pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2
        dist = np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
        offset = int(dist * random.uniform(0.1, 0.35))
        cx = mid_x + random.randint(-offset, offset)
        cy = mid_y + random.randint(-offset, offset)

        if random.random() > 0.4:
            # 绘制贝塞尔曲线
            pts = []
            for t in np.linspace(0, 1, 10):
                x = int((1 - t) ** 2 * pt1[0] + 2 * (1 - t) * t * cx + t ** 2 * pt2[0])
                y = int((1 - t) ** 2 * pt1[1] + 2 * (1 - t) * t * cy + t ** 2 * pt2[1])
                pts.append([x, y])

            pts_array = np.array(pts, np.int32).reshape((-1, 1, 2))
            cv2.polylines(img, [pts_array], False, color, thickness, cv2.LINE_AA)
        else:
            cv2.line(img, pt1, (cx, cy), color, thickness, cv2.LINE_AA)
            cv2.line(img, (cx, cy), pt2, color, thickness, cv2.LINE_AA)
            if random.random() > 0.6:
                # 确保红色值也是整数
                red_color = core.cv_red
                if not isinstance(red_color, tuple) or len(red_color) != 3:
                    red_color = (0, 0, 255)  # 默认红色
                red_color = (int(red_color[0]), int(red_color[1]), int(red_color[2]))
                cv2.circle(img, (cx, cy), max(1, int(1.5 * core.scale)), red_color, -1)
    else:
        cv2.line(img, pt1, pt2, color, thickness, cv2.LINE_AA)