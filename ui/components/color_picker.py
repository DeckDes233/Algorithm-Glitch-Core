# ui/components/color_picker.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import gradio as gr
from typing import Tuple, Callable
from ui.utils import rgba_to_hex, hex_to_rgba


def create_color_picker(
        label: str,
        default_color: Tuple[int, int, int, int],
        on_change: Callable = None
) -> gr.ColorPicker:
    """创建带RGBA支持的颜色选择器"""

    def color_change_handler(color_hex, *args):
        rgba = hex_to_rgba(color_hex)
        if on_change:
            return on_change(rgba, *args)
        return color_hex

    color_picker = gr.ColorPicker(
        label=label,
        value=rgba_to_hex(default_color),
        interactive=True
    )

    if on_change:
        color_picker.change(
            fn=color_change_handler,
            inputs=[color_picker],
            outputs=[color_picker]
        )

    return color_picker


def create_rgba_sliders(
        label: str,
        default_color: Tuple[int, int, int, int],
        on_change: Callable = None
) -> Tuple[gr.Slider, gr.Slider, gr.Slider, gr.Slider]:
    """创建RGBA滑块组"""

    with gr.Row():
        r_slider = gr.Slider(
            minimum=0, maximum=255, value=default_color[0], step=1,
            label=f"{label} R"
        )
        g_slider = gr.Slider(
            minimum=0, maximum=255, value=default_color[1], step=1,
            label=f"{label} G"
        )
        b_slider = gr.Slider(
            minimum=0, maximum=255, value=default_color[2], step=1,
            label=f"{label} B"
        )
        a_slider = gr.Slider(
            minimum=0, maximum=255, value=default_color[3], step=1,
            label=f"{label} A"
        )

    return r_slider, g_slider, b_slider, a_slider