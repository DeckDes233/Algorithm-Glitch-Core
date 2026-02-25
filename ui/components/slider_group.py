# ui/components/slider_group.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import gradio as gr
from typing import Tuple, List, Any


def create_range_sliders(
        label: str,
        default_range: Tuple[Any, Any],
        min_value: Any,
        max_value: Any,
        step: Any = 1
) -> Tuple[gr.Number, gr.Number]:
    """创建范围滑块组"""

    with gr.Row():
        min_slider = gr.Number(
            label=f"{label} 最小值",
            value=default_range[0],
            minimum=min_value,
            maximum=max_value,
            step=step
        )
        max_slider = gr.Number(
            label=f"{label} 最大值",
            value=default_range[1],
            minimum=min_value,
            maximum=max_value,
            step=step
        )

    return min_slider, max_slider


def create_probability_slider(
        label: str,
        default_value: float,
        description: str = ""
) -> gr.Slider:
    """创建概率滑块"""
    return gr.Slider(
        label=label,
        info=description,
        value=default_value,
        minimum=0,
        maximum=1,
        step=0.01
    )


def create_weight_sliders(
        weights_dict: dict,
        on_change: Callable = None
) -> dict:
    """创建权重滑块组"""

    sliders = {}
    for key, value in weights_dict.items():
        sliders[key] = gr.Slider(
            label=f"{key} 权重",
            value=value,
            minimum=0,
            maximum=10,
            step=1
        )

    return sliders