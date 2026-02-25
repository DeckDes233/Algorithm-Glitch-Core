# ui/tabs/preview.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import gradio as gr
import os
import tempfile
from PIL import Image
import numpy as np
import time

from core.renderer import ConfigurableCyberCore
from ui.utils import get_example_images


def preview_with_config(
        example_image,
        config,
        font_path,
        seed,
        debug
):
    """使用当前配置预览效果"""

    # 如果没有选择示例图片，返回错误
    if example_image is None:
        return None, "❌ 错误：请选择示例图片"

    # 检查示例图片是否存在
    if not os.path.exists(example_image):
        return None, f"❌ 错误：示例图片不存在 - {example_image}"

    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        output_path = tmp.name

    # 处理图片
    try:
        start_time = time.time()

        core = ConfigurableCyberCore(example_image, font_path, config, seed, debug)
        core.run(output_path)

        elapsed_time = time.time() - start_time
        stats = core.get_stats()

        stats_text = f"""
        ✅ **预览效果**

        **处理信息:**
        - 种子: {seed}
        - 框数量: {stats['boxes_drawn']}
        - 空间错位框: {stats['warp_boxes']}
        - 框间连线: {stats['box_connections']}
        - 文本块: {stats['text_blocks']}
        - 处理时间: {elapsed_time:.2f}秒
        """

        return output_path, stats_text

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"预览失败: {error_details}")
        return None, f"❌ 处理失败：{str(e)}"


def create_preview_tab(config_state, font_path_state):
    """创建预览标签页"""

    # 获取示例图片
    example_images = get_example_images()
    default_example = example_images[0] if example_images else None

    with gr.Row():
        with gr.Column(scale=1):
            # 示例图片选择
            example_dropdown = gr.Dropdown(
                choices=example_images,
                label="选择示例图片",
                value=default_example,
                interactive=True
            )

            # 如果没有示例图片，显示提示
            if not example_images:
                gr.Markdown("⚠️ 没有找到示例图片，请先在 static/examples 目录放置示例图片")

            # 参数设置
            seed_input = gr.Number(
                value=42,
                label="种子",
                precision=0,
                minimum=1,
                maximum=9999999
            )

            debug_check = gr.Checkbox(value=False, label="调试模式")

            # 预览按钮
            preview_btn = gr.Button("👁️ 预览效果", variant="primary", size="lg")

            # 快速参数调整
            gr.Markdown("### ⚡ 快速参数调整")

            with gr.Row():
                box_count_min = gr.Slider(
                    minimum=5, maximum=50, value=18, step=1,
                    label="最小框数"
                )
                box_count_max = gr.Slider(
                    minimum=10, maximum=80, value=30, step=1,
                    label="最大框数"
                )

            with gr.Row():
                warp_intensity = gr.Slider(
                    minimum=0, maximum=1.5, value=0.7, step=0.05,
                    label="错位强度"
                )
                line_connect_chance = gr.Slider(
                    minimum=0, maximum=1, value=0.8, step=0.05,
                    label="连线概率"
                )

            with gr.Row():
                enable_dof = gr.Checkbox(value=True, label="启用景深")
                use_extended_errors = gr.Checkbox(value=True, label="启用扩展错误")

            # 重置按钮
            reset_btn = gr.Button("🔄 重置参数", size="sm")

        with gr.Column(scale=1):
            preview_image = gr.Image(
                type="filepath",
                label="预览结果",
                height=500,
                show_label=True,
                interactive=False
            )
            preview_stats = gr.Markdown(label="预览信息")

    # 更新配置并预览的函数
    def update_and_preview(example, config, font, seed, debug,
                           box_min, box_max, warp_int, line_conn,
                           dof, errors):
        """更新配置并预览"""

        # 创建配置的副本以避免修改原始配置
        import copy
        temp_config = copy.deepcopy(config)

        # 更新配置
        temp_config.box_count = (int(box_min), int(box_max))
        temp_config.warp_intensity = warp_int
        temp_config.box_line_connect_chance = line_conn
        temp_config.enable_depth_of_field = dof
        temp_config.use_extended_errors = errors

        # 预览
        return preview_with_config(example, temp_config, font, seed, debug)

    # 预览按钮点击事件
    preview_btn.click(
        fn=update_and_preview,
        inputs=[
            example_dropdown, config_state, font_path_state,
            seed_input, debug_check,
            box_count_min, box_count_max,
            warp_intensity, line_connect_chance,
            enable_dof, use_extended_errors
        ],
        outputs=[preview_image, preview_stats]
    )

    # 重置参数的函数
    def reset_parameters():
        """重置所有参数到默认值"""
        return [
            18, 30,  # box_count_min, box_count_max
            0.7, 0.8,  # warp_intensity, line_connect_chance
            True, True  # enable_dof, use_extended_errors
        ]

    reset_btn.click(
        fn=reset_parameters,
        outputs=[
            box_count_min, box_count_max,
            warp_intensity, line_connect_chance,
            enable_dof, use_extended_errors
        ]
    )

    # 当示例图片改变时，自动更新预览（可选）
    example_dropdown.change(
        fn=lambda x: (x, "请点击预览按钮查看效果"),
        inputs=[example_dropdown],
        outputs=[preview_image, preview_stats]
    )

    gr.Markdown("""
    ### 💡 提示
    - 选择示例图片后，点击预览按钮查看效果
    - 调整参数后需要再次点击预览按钮
    - 预览结果不会保存，仅用于测试参数效果
    - 处理时间取决于图片大小和参数复杂度
    """)