# ui/tabs/single.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import gradio as gr
import os
import random
from pathlib import Path

from core.renderer import ConfigurableCyberCore


def process_single_image(input_img, config, font_path, seed, debug):
    """处理单张图片"""

    # 检查是否上传了图片
    if input_img is None:
        return None, "❌ 错误：请先上传图片", -1, None

    # 生成输出路径
    output_dir = "outputs/single"
    os.makedirs(output_dir, exist_ok=True)

    # 保存输入图片
    temp_input = os.path.join(output_dir, "temp_input.png")
    try:
        input_img.save(temp_input)
    except Exception as e:
        return None, f"❌ 保存临时文件失败: {str(e)}", -1, None

    # 生成输出文件名
    if seed == -1:
        seed_used = random.randint(1, 1000000)
    else:
        seed_used = int(seed)

    output_path = os.path.join(output_dir, f"output_seed{seed_used}.png")
    output_filename = os.path.basename(output_path)

    # 处理图片
    try:
        core = ConfigurableCyberCore(temp_input, font_path, config, seed_used, debug)
        core.run(output_path)

        stats = core.get_stats()
        stats_text = f"""
        ✅ **处理完成！**

        **统计信息:**
        - 种子: {seed_used}
        - 框数量: {stats['boxes_drawn']}
        - 空间错位框: {stats['warp_boxes']}
        - 框间连线: {stats['box_connections']}
        - 文本块: {stats['text_blocks']}
        - 处理时间: {stats['processing_time']:.2f}秒

        **输出文件:** {output_filename}
        """

        return output_path, stats_text, seed_used, output_path

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"处理失败: {error_details}")
        return None, f"❌ 处理失败: {str(e)}", seed_used, None


def create_single_tab(config_state, font_path_state):
    """创建单张处理标签页"""

    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(
                type="pil",
                label="输入图片",
                show_label=True,
                interactive=True,
                height=300
            )

            with gr.Row():
                seed_input = gr.Number(
                    value=-1,
                    label="随机种子 (-1 表示随机)",
                    precision=0,
                    minimum=-1,
                    maximum=9999999
                )
                debug_check = gr.Checkbox(value=False, label="调试模式")

            process_btn = gr.Button("🚀 生成AlgorithmGlitchCore风格", variant="primary")

            # 添加清除按钮
            clear_btn = gr.Button("🗑️ 清除", variant="secondary")

        with gr.Column(scale=1):
            # 输出图片 - Gradio 6.0 兼容的配置
            output_image = gr.Image(
                type="filepath",
                label="输出结果",
                show_label=True,
                interactive=False,
                height=400,
                width=600,
                container=True  # 添加容器以便显示边框
            )

            # 添加图片操作按钮
            with gr.Row():
                # 使用 File 组件来实现下载功能
                download_file = gr.File(
                    label="点击下载图片",
                    visible=False
                )
                show_download_btn = gr.Button("📥 显示下载链接", size="sm")
                zoom_btn = gr.Button("🔍 放大查看", size="sm")

            stats_output = gr.Markdown(label="处理信息")
            seed_used = gr.Number(value=0, label="实际使用的种子", visible=False)

            # 用于存储当前输出图片路径的State
            current_image_path = gr.State(None)

    # 处理按钮点击事件
    process_result = process_btn.click(
        fn=process_single_image,
        inputs=[input_image, config_state, font_path_state, seed_input, debug_check],
        outputs=[output_image, stats_output, seed_used, current_image_path]
    )

    # 显示下载链接功能
    def show_download_link(image_path):
        if image_path and os.path.exists(image_path):
            return gr.update(visible=True, value=image_path)
        return gr.update(visible=False)

    show_download_btn.click(
        fn=show_download_link,
        inputs=[current_image_path],
        outputs=[download_file]
    )

    # 放大查看功能 - 在新窗口中打开图片（通过更新图片尺寸）
    def zoom_image(image_path):
        if image_path and os.path.exists(image_path):
            return gr.update(value=image_path, height=800, width=1200)
        return gr.update()

    zoom_btn.click(
        fn=zoom_image,
        inputs=[current_image_path],
        outputs=[output_image]
    )

    # 添加一个恢复按钮来恢复原始大小
    def reset_size(image_path):
        if image_path and os.path.exists(image_path):
            return gr.update(value=image_path, height=400, width=600)
        return gr.update()

    reset_btn = gr.Button("🔄 恢复大小", size="sm", visible=False)

    def toggle_reset_button(show):
        return gr.update(visible=show)

    zoom_btn.click(
        fn=lambda: True,
        outputs=[reset_btn]
    )

    reset_btn.click(
        fn=reset_size,
        inputs=[current_image_path],
        outputs=[output_image]
    ).then(
        fn=lambda: False,
        outputs=[reset_btn]
    )

    # 清除按钮功能
    def clear_all():
        return None, None, "", -1, None, gr.update(visible=False)

    clear_btn.click(
        fn=clear_all,
        outputs=[input_image, output_image, stats_output, seed_input, current_image_path, download_file]
    )

    # 添加示例图片
    gr.Examples(
        examples=[
            ["static/examples/example1.jpg"],
            ["static/examples/example2.jpg"],
        ],
        inputs=input_image,
        label="点击使用示例图片"
    )

    # 添加使用说明
    gr.Markdown("""
    ### 📝 使用说明
    1. 上传一张图片或点击示例图片
    2. 选择随机种子（-1表示完全随机）
    3. 点击生成按钮
    4. 等待处理完成

    ### 🖼️ 图片查看功能
    - **点击图片**：可以放大查看（Gradio内置）
    - **显示下载链接**：点击后显示下载按钮
    - **放大查看**：以更大尺寸显示图片
    - **恢复大小**：恢复原始尺寸
    """)