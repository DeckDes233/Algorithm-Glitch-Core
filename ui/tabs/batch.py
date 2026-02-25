# ui/tabs/batch.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import gradio as gr
import os
import random
from pathlib import Path
from typing import List, Tuple


def process_batch_images(
        input_dir: str,
        config,
        font_path: str,
        seeds_input: str,
        debug: bool,
        progress=gr.Progress()
) -> Tuple[str, str, List[str]]:
    """批量处理图片"""

    if not os.path.exists(input_dir):
        return f"错误：输入目录 '{input_dir}' 不存在", "", []

    # 获取所有图片
    image_files = [f for f in os.listdir(input_dir)
                   if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    if not image_files:
        return f"错误：目录 '{input_dir}' 中没有图片文件", "", []

    # 解析种子
    if seeds_input.strip():
        try:
            seeds = [int(s.strip()) for s in seeds_input.split(',')]
        except:
            seeds = []
    else:
        seeds = []

    # 创建输出目录
    output_dir = "outputs/batch"
    os.makedirs(output_dir, exist_ok=True)

    # 处理图片
    results = []
    stats_summary = []

    progress(0, desc="开始批量处理...")

    for i, filename in enumerate(image_files):
        progress((i + 1) / len(image_files), desc=f"处理 {filename}")

        # 确定种子
        if i < len(seeds):
            seed = seeds[i]
        else:
            seed = random.randint(1, 1000000)

        # 处理图片
        input_path = os.path.join(input_dir, filename)
        output_filename = f"cyber_{seed}_{filename}"
        output_path = os.path.join(output_dir, output_filename)

        try:
            core = ConfigurableCyberCore(input_path, font_path, config, seed, debug)
            core.run(output_path)

            stats = core.get_stats()
            stats_summary.append(f"{filename}: 种子={seed}, 框数={stats['boxes_drawn']}")
            results.append(output_path)
        except Exception as e:
            stats_summary.append(f"{filename}: 处理失败 - {str(e)}")

    # 生成结果
    summary = "\n".join([
        f"处理完成！共 {len(results)}/{len(image_files)} 张图片成功",
        "",
        *stats_summary
    ])

    return summary, output_dir, results


def get_directory_files(directory):
    """获取目录中的文件列表"""
    if not os.path.exists(directory):
        return []

    files = [f for f in os.listdir(directory)
             if os.path.isfile(os.path.join(directory, f)) and
             f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    return files


def create_batch_tab(config_state, font_path_state):
    """创建批量处理标签页"""

    with gr.Row():
        with gr.Column(scale=1):
            input_dir = gr.Textbox(
                label="输入目录",
                placeholder="请输入包含图片的目录路径",
                value="inputs"
            )

            seeds_input = gr.Textbox(
                label="随机种子列表（用逗号分隔，可选）",
                placeholder="例如: 42,123,456",
                value=""
            )

            with gr.Row():
                debug_check = gr.Checkbox(value=False, label="调试模式")
                refresh_btn = gr.Button("🔄 刷新文件列表")

            process_btn = gr.Button("🚀 批量生成", variant="primary")

            # 使用 Dropdown 替代 FileExplorer
            file_list = gr.Dropdown(
                label="目录中的文件",
                choices=[],
                multiselect=True,
                interactive=False
            )

        with gr.Column(scale=1):
            summary_output = gr.Textbox(
                label="处理摘要",
                lines=10,
                interactive=False
            )

            output_dir_display = gr.Textbox(
                label="输出目录",
                interactive=False
            )

            # Gradio 6.0 兼容的Gallery组件
            output_gallery = gr.Gallery(
                label="生成结果",
                columns=3,
                rows=2,
                height="auto",
                object_fit="contain",  # 确保图片完整显示
                show_label=True
            )

            # 添加选中的图片放大查看
            with gr.Row():
                selected_image = gr.Image(
                    label="选中的图片 (点击上方图片选择)",
                    type="filepath",
                    height=300,
                    show_label=True
                )

                # 下载选中的图片
                download_selected = gr.File(
                    label="下载选中图片",
                    visible=False
                )
                download_btn = gr.Button("📥 下载选中图片", size="sm")

    # 刷新文件列表
    def update_file_list(directory):
        files = get_directory_files(directory)
        return gr.Dropdown(choices=files)

    refresh_btn.click(
        fn=update_file_list,
        inputs=[input_dir],
        outputs=[file_list]
    )

    # 处理批量图片
    process_btn.click(
        fn=process_batch_images,
        inputs=[input_dir, config_state, font_path_state, seeds_input, debug_check],
        outputs=[summary_output, output_dir_display, output_gallery]
    )

    # 当点击Gallery中的图片时，在selected_image中显示
    def select_image(evt: gr.SelectData, gallery_images):
        """当在Gallery中选择图片时"""
        if gallery_images and evt.index < len(gallery_images):
            return gallery_images[evt.index]
        return None

    output_gallery.select(
        fn=select_image,
        inputs=[output_gallery],
        outputs=[selected_image]
    )

    # 下载选中的图片
    def prepare_download(selected_img):
        if selected_img:
            return gr.update(visible=True, value=selected_img)
        return gr.update(visible=False)

    download_btn.click(
        fn=prepare_download,
        inputs=[selected_image],
        outputs=[download_selected]
    )

    # 初始加载时也更新文件列表
    input_dir.change(
        fn=update_file_list,
        inputs=[input_dir],
        outputs=[file_list]
    )

    gr.Markdown("""
    ### 📝 使用说明
    1. 将需要处理的图片放入输入目录
    2. 可以选择指定种子列表（每张图片一个种子）
    3. 点击批量生成开始处理
    4. 处理结果将保存在 outputs/batch 目录

    ### 🖼️ 图片查看功能
    - **点击缩略图**：可以在下方放大查看
    - **下载按钮**：点击后显示下载链接
    """)