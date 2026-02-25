# app.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目根目录到系统路径
sys.path.insert(0, str(Path(__file__).parent))

import gradio as gr
import random

from config import CyberConfig
from core.renderer import ConfigurableCyberCore
from ui.tabs.single import create_single_tab
from ui.tabs.batch import create_batch_tab
from ui.tabs.config import create_config_tab
from ui.tabs.preview import create_preview_tab
from ui.utils import load_config, save_config, preview_config

# 创建必要的目录
os.makedirs("inputs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("outputs/single", exist_ok=True)
os.makedirs("outputs/batch", exist_ok=True)
os.makedirs("configs", exist_ok=True)
os.makedirs("static/examples", exist_ok=True)


# 默认字体路径 - 检查系统可用的字体
def get_default_font():
    """获取系统默认的等宽字体"""
    if os.name == 'nt':  # Windows
        possible_fonts = [
            "C:/Windows/Fonts/courbd.ttf",  # Courier New Bold
            "C:/Windows/Fonts/cour.ttf",  # Courier New
            "C:/Windows/Fonts/consola.ttf",  # Consolas
            "C:/Windows/Fonts/verdana.ttf",  # Verdana
            "C:/Windows/Fonts/arial.ttf",  # Arial
        ]
    else:  # Linux/Mac
        possible_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/System/Library/Fonts/Menlo.ttc",  # Mac
        ]

    for font_path in possible_fonts:
        if os.path.exists(font_path):
            return font_path

    return None  # 如果没有找到字体，返回None，使用PIL默认字体


DEFAULT_FONT = get_default_font()
if DEFAULT_FONT:
    print(f"✅ 使用字体: {DEFAULT_FONT}")
else:
    print("⚠️ 未找到系统字体，将使用PIL默认字体")


def create_interface():
    """创建Gradio界面"""

    # Gradio 6.0+ 中 theme 参数移到了 launch() 方法
    with gr.Blocks(title="AlgorithmGlitchCore图像生成器") as demo:
        gr.Markdown("""
        # 🌆 AlgorithmGlitchCore风格图像生成器
        为你的图片添加AlgorithmGlitchCore风格的故障艺术效果
        """)

        # 全局状态
        config_state = gr.State(CyberConfig())
        font_path_state = gr.State(DEFAULT_FONT)

        with gr.Tabs():
            # 单张处理标签页
            with gr.TabItem("🖼️ 单张处理"):
                create_single_tab(config_state, font_path_state)

            # 批量处理标签页
            with gr.TabItem("📁 批量处理"):
                create_batch_tab(config_state, font_path_state)

            # 配置管理标签页
            with gr.TabItem("⚙️ 配置管理"):
                create_config_tab(config_state)

            # 预览标签页
            with gr.TabItem("👁️ 效果预览"):
                create_preview_tab(config_state, font_path_state)

        gr.Markdown("""
        ---
        ### 📝 使用说明
        - 在配置管理中可以调整所有参数
        - 支持单张处理和批量处理
        - 可以保存/加载配置模板
        - 随机种子确保结果可重现
        """)

    return demo


# 创建 demo 实例
demo = create_interface()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        theme=gr.themes.Soft()  # theme 参数移到这里
    )