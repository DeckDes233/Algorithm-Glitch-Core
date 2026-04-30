# ui/tabs/config.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import gradio as gr
import json
import os
from typing import Dict, Any

from config import CyberConfig
from ui.utils import preview_config, save_config, load_config, rgba_to_hex, hex_to_rgba


def create_config_tab(config_state):
    """创建配置管理标签页"""

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 🎨 当前配置预览")
            preview_btn = gr.Button("👁️ 刷新预览")
            preview_output = gr.Markdown()

            # 添加重置按钮
            reset_btn = gr.Button("🔄 重置为默认配置")

        with gr.Column(scale=1):
            gr.Markdown("### 💾 保存/加载配置")
            config_name = gr.Textbox(value="my_config", label="配置名称")
            save_status = gr.Textbox(label="状态", interactive=False)
            save_btn = gr.Button("💾 保存配置")

            load_dropdown = gr.Dropdown(
                choices=get_config_list(),
                label="选择配置",
                interactive=True
            )
            load_btn = gr.Button("📂 加载配置")
            refresh_btn = gr.Button("🔄 刷新列表")

    with gr.Row():
        gr.Markdown("### ⚙️ 详细参数调整")
        gr.Markdown("修改下面的参数会自动更新配置")

    # 创建所有配置控件
    color_inputs = create_color_config()
    box_inputs = create_box_config()
    warp_inputs = create_warp_config()
    noise_inputs = create_noise_config()
    text_inputs = create_text_config()
    dof_inputs = create_dof_config()
    error_inputs = create_error_config()

    # 收集所有输入控件
    all_inputs = {}
    all_inputs.update(color_inputs)
    all_inputs.update(box_inputs)
    all_inputs.update(warp_inputs)
    all_inputs.update(noise_inputs)
    all_inputs.update(text_inputs)
    all_inputs.update(dof_inputs)
    all_inputs.update(error_inputs)

    # 创建输入列表用于事件
    input_list = list(all_inputs.values())
    input_names = list(all_inputs.keys())

    # 预览按钮事件
    preview_btn.click(
        fn=preview_config,
        inputs=[config_state],
        outputs=[preview_output]
    )

    # 重置按钮事件
    reset_btn.click(
        fn=reset_to_default,
        outputs=[config_state] + input_list
    ).then(
        fn=preview_config,
        inputs=[config_state],
        outputs=[preview_output]
    ).then(
        fn=lambda: "✅ 已重置为默认配置",
        outputs=[save_status]
    )

    # 保存配置
    save_btn.click(
        fn=save_config_ui,
        inputs=[config_state, config_name],
        outputs=[save_status]
    ).then(
        fn=refresh_config_list,
        outputs=[load_dropdown]
    )

    # 加载配置
    load_btn.click(
        fn=load_config_ui,
        inputs=[load_dropdown],
        outputs=[config_state] + input_list + [save_status]
    ).then(
        fn=preview_config,
        inputs=[config_state],
        outputs=[preview_output]
    )

    # 刷新配置列表
    refresh_btn.click(
        fn=refresh_config_list,
        outputs=[load_dropdown]
    )

    # 为每个输入控件添加变更事件
    for input_name, input_component in all_inputs.items():
        input_component.change(
            fn=update_config_from_input,
            inputs=[config_state, gr.State(input_name), input_component],
            outputs=[config_state]
        ).then(
            fn=preview_config,
            inputs=[config_state],
            outputs=[preview_output]
        )

    # 初始预览
    preview_btn.click(
        fn=preview_config,
        inputs=[config_state],
        outputs=[preview_output]
    )


def create_color_config() -> Dict[str, gr.Component]:
    """创建颜色配置UI"""
    inputs = {}

    with gr.TabItem("🎨 颜色"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### 文字颜色")
                inputs['color_error_text'] = gr.ColorPicker(
                    value="#FF3232",
                    label="错误文字颜色",
                    info="RGBA格式，例如 #FF3232"
                )
                inputs['color_normal_text'] = gr.ColorPicker(
                    value="#FFFFFF",
                    label="普通文字颜色"
                )

                gr.Markdown("#### 边框颜色")
                inputs['color_border'] = gr.ColorPicker(
                    value="#FFFFFF",
                    label="边框颜色"
                )
                inputs['color_line'] = gr.ColorPicker(
                    value="#FFFFFFB4",
                    label="连线颜色"
                )

            with gr.Column():
                gr.Markdown("#### 其他颜色")
                inputs['color_warning'] = gr.ColorPicker(
                    value="#FF3232",
                    label="警告颜色"
                )
                inputs['color_float'] = gr.ColorPicker(
                    value="#FFFFFF",
                    label="浮点数颜色"
                )
                inputs['mesh_color'] = gr.ColorPicker(
                    value="#FFFFFFC8",
                    label="网格颜色"
                )

    return inputs


def create_box_config() -> Dict[str, gr.Component]:
    """创建框配置UI"""
    inputs = {}

    with gr.TabItem("📦 框配置"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### 框数量范围")
                inputs['box_count_min'] = gr.Slider(
                    minimum=1, maximum=50, value=18, step=1,
                    label="最小框数"
                )
                inputs['box_count_max'] = gr.Slider(
                    minimum=2, maximum=80, value=30, step=1,
                    label="最大框数"
                )

                gr.Markdown("#### 框大小范围")
                inputs['box_size_min'] = gr.Slider(
                    minimum=10, maximum=200, value=40, step=5,
                    label="最小大小"
                )
                inputs['box_size_max'] = gr.Slider(
                    minimum=20, maximum=400, value=150, step=5,
                    label="最大大小"
                )

                inputs['box_border_thickness'] = gr.Slider(
                    minimum=1, maximum=5, value=1, step=1,
                    label="边框粗细"
                )

            with gr.Column():
                gr.Markdown("#### 连线设置")
                inputs['box_line_connect_chance'] = gr.Slider(
                    minimum=0, maximum=1, value=0.8, step=0.05,
                    label="连线概率"
                )
                inputs['box_line_jitter_chance'] = gr.Slider(
                    minimum=0, maximum=1, value=0.3, step=0.05,
                    label="抖动概率"
                )
                inputs['box_line_max_distance'] = gr.Slider(
                    minimum=50, maximum=500, value=300, step=10,
                    label="最大连线距离"
                )
                inputs['box_line_thickness'] = gr.Slider(
                    minimum=1, maximum=5, value=1, step=1,
                    label="连线粗细"
                )

        with gr.Row():
            with gr.Column():
                gr.Markdown("#### 框类型权重")
                inputs['box_type_plain'] = gr.Slider(
                    minimum=0, maximum=10, value=3, step=1,
                    label="普通框"
                )
                inputs['box_type_invert'] = gr.Slider(
                    minimum=0, maximum=10, value=2, step=1,
                    label="反色框"
                )
                inputs['box_type_bios'] = gr.Slider(
                    minimum=0, maximum=10, value=4, step=1,
                    label="BIOS框"
                )
                inputs['box_type_space_warp'] = gr.Slider(
                    minimum=0, maximum=10, value=3, step=1,
                    label="空间错位框"
                )

            with gr.Column():
                gr.Markdown("#### 浮点数显示")
                inputs['box_float_display'] = gr.Checkbox(
                    value=True, label="显示浮点数"
                )
                inputs['box_float_precision'] = gr.Slider(
                    minimum=0, maximum=6, value=3, step=1,
                    label="小数位数"
                )

    return inputs


def create_warp_config() -> Dict[str, gr.Component]:
    """创建空间错位配置UI"""
    inputs = {}

    with gr.TabItem("🌌 空间错位"):
        with gr.Row():
            with gr.Column():
                inputs['warp_intensity'] = gr.Slider(
                    minimum=0, maximum=1.5, value=0.7, step=0.05,
                    label="错位强度"
                )
                inputs['warp_segments'] = gr.Slider(
                    minimum=2, maximum=20, value=10, step=1,
                    label="错位分段数"
                )
                inputs['warp_glitch_chance'] = gr.Slider(
                    minimum=0, maximum=1, value=0.8, step=0.05,
                    label="错位概率"
                )

            with gr.Column():
                inputs['warp_shift_min'] = gr.Slider(
                    minimum=1, maximum=20, value=5, step=1,
                    label="最小偏移量"
                )
                inputs['warp_shift_max'] = gr.Slider(
                    minimum=5, maximum=50, value=20, step=1,
                    label="最大偏移量"
                )

                with gr.Row():
                    inputs['warp_color_shift'] = gr.Checkbox(
                        value=True, label="颜色通道错位"
                    )
                    inputs['warp_scanline_jitter'] = gr.Checkbox(
                        value=True, label="扫描线抖动"
                    )

    return inputs


def create_noise_config() -> Dict[str, gr.Component]:
    """创建噪声效果配置UI"""
    inputs = {}

    with gr.TabItem("🌊 噪声效果"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("#### Perlin噪声")
                inputs['enable_noise'] = gr.Checkbox(
                    value=True, label="启用噪声效果"
                )
                inputs['noise_perlin_scale'] = gr.Slider(
                    minimum=10, maximum=200, value=80, step=5,
                    label="Perlin缩放", info="值越大纹理越细腻"
                )
                inputs['noise_perlin_octaves'] = gr.Slider(
                    minimum=1, maximum=8, value=4, step=1,
                    label="Perlin八度", info="细节层次数"
                )
                inputs['noise_perlin_intensity'] = gr.Slider(
                    minimum=0, maximum=80, value=30, step=1,
                    label="Perlin强度"
                )

            with gr.Column():
                gr.Markdown("#### RGB通道独立噪声")
                inputs['noise_rgb_separate'] = gr.Checkbox(
                    value=True, label="启用RGB独立噪声"
                )
                inputs['noise_rgb_r_intensity'] = gr.Slider(
                    minimum=0, maximum=80, value=35, step=1,
                    label="红色通道强度"
                )
                inputs['noise_rgb_g_intensity'] = gr.Slider(
                    minimum=0, maximum=80, value=25, step=1,
                    label="绿色通道强度"
                )
                inputs['noise_rgb_b_intensity'] = gr.Slider(
                    minimum=0, maximum=80, value=30, step=1,
                    label="蓝色通道强度"
                )

        with gr.Row():
            with gr.Column():
                gr.Markdown("#### 扫描线噪声")
                inputs['noise_scanline_enabled'] = gr.Checkbox(
                    value=True, label="启用扫描线噪声"
                )
                inputs['noise_scanline_intensity'] = gr.Slider(
                    minimum=0, maximum=60, value=20, step=1,
                    label="扫描线强度"
                )
                inputs['noise_scanline_frequency'] = gr.Slider(
                    minimum=0.1, maximum=3.0, value=0.5, step=0.1,
                    label="扫描线频率"
                )

            with gr.Column():
                gr.Markdown("#### 全局控制")
                inputs['noise_strength'] = gr.Slider(
                    minimum=0, maximum=2.0, value=1.0, step=0.05,
                    label="噪声总强度", info="统一缩放所有噪声效果"
                )

    return inputs


def create_text_config() -> Dict[str, gr.Component]:
    """创建文字配置UI"""
    inputs = {}

    with gr.TabItem("📝 文字"):
        with gr.Row():
            with gr.Column():
                inputs['title_erosion_rate'] = gr.Slider(
                    minimum=0, maximum=1, value=0.33, step=0.05,
                    label="标题侵蚀率"
                )
                inputs['node_text_chance'] = gr.Slider(
                    minimum=0, maximum=1, value=0.35, step=0.05,
                    label="节点文字概率"
                )
                inputs['hud_line_chance'] = gr.Slider(
                    minimum=0, maximum=1, value=0.6, step=0.05,
                    label="HUD连线概率"
                )

            with gr.Column():
                gr.Markdown("#### 文字块数量")
                inputs['log_blocks_min'] = gr.Slider(
                    minimum=1, maximum=30, value=4, step=1,
                    label="最小块数"
                )
                inputs['log_blocks_max'] = gr.Slider(
                    minimum=5, maximum=50, value=28, step=1,
                    label="最大块数"
                )

    return inputs


def create_dof_config() -> Dict[str, gr.Component]:
    """创建景深效果配置UI"""
    inputs = {}

    with gr.TabItem("🌫️ 景深效果"):
        with gr.Row():
            with gr.Column():
                inputs['enable_depth_of_field'] = gr.Checkbox(
                    value=True, label="启用景深效果"
                )
                inputs['depth_blur_amount'] = gr.Slider(
                    minimum=0, maximum=5, value=1.5, step=0.1,
                    label="模糊强度"
                )
                inputs['depth_darken_amount'] = gr.Slider(
                    minimum=0, maximum=1, value=0.7, step=0.05,
                    label="变暗强度"
                )

            with gr.Column():
                inputs['depth_focus_radius'] = gr.Slider(
                    minimum=0, maximum=1, value=0.3, step=0.05,
                    label="焦点区域半径"
                )
                inputs['depth_fade_start'] = gr.Slider(
                    minimum=0, maximum=1, value=0.2, step=0.05,
                    label="淡出起始距离"
                )

    return inputs


def create_error_config() -> Dict[str, gr.Component]:
    """创建错误消息配置UI"""
    inputs = {}

    with gr.TabItem("🎯 错误消息"):
        with gr.Row():
            with gr.Column():
                inputs['use_extended_errors'] = gr.Checkbox(
                    value=True, label="使用扩展错误消息"
                )

    return inputs


def get_config_list() -> list:
    """获取配置列表"""
    config_dir = "configs"
    os.makedirs(config_dir, exist_ok=True)
    configs = [f.replace(".json", "") for f in os.listdir(config_dir)
               if f.endswith(".json")]
    return configs if configs else ["(无保存的配置)"]


def refresh_config_list():
    """刷新配置列表"""
    configs = get_config_list()
    return gr.Dropdown(choices=configs, value=configs[0] if configs else None)


def save_config_ui(config, name):
    """保存配置"""
    try:
        save_config(config, f"configs/{name}.json")
        return f"✅ 配置已保存为 {name}"
    except Exception as e:
        return f"❌ 保存失败: {str(e)}"


def load_config_ui(name):
    """加载配置"""
    try:
        if name == "(无保存的配置)" or not os.path.exists(f"configs/{name}.json"):
            return [CyberConfig()] + [None] * 100 + ["⚠️ 使用默认配置"]  # 返回默认配置

        config = load_config(f"configs/{name}.json")

        # 将配置转换为UI控件的值
        ui_values = config_to_ui_values(config)

        return [config] + ui_values + [f"✅ 配置 {name} 已加载"]
    except Exception as e:
        return [CyberConfig()] + [None] * 100 + [f"❌ 加载失败: {str(e)}"]


def reset_to_default():
    """重置为默认配置"""
    default_config = CyberConfig()
    ui_values = config_to_ui_values(default_config)
    return [default_config] + ui_values


def config_to_ui_values(config: CyberConfig) -> list:
    """将配置对象转换为UI控件的值列表"""
    values = []

    # 颜色值
    values.append(rgba_to_hex(config.color_error_text))
    values.append(rgba_to_hex(config.color_normal_text))
    values.append(rgba_to_hex(config.color_border))
    values.append(rgba_to_hex(config.color_line))
    values.append(rgba_to_hex(config.color_warning))
    values.append(rgba_to_hex(config.color_float))
    values.append(rgba_to_hex(config.mesh_color))

    # 框配置
    values.append(config.box_count[0])  # box_count_min
    values.append(config.box_count[1])  # box_count_max
    values.append(config.box_size_range[0])  # box_size_min
    values.append(config.box_size_range[1])  # box_size_max
    values.append(config.box_border_thickness)
    values.append(config.box_line_connect_chance)
    values.append(config.box_line_jitter_chance)
    values.append(config.box_line_max_distance)
    values.append(config.box_line_thickness)
    values.append(config.box_type_weights.get('plain', 3))
    values.append(config.box_type_weights.get('invert', 2))
    values.append(config.box_type_weights.get('bios', 4))
    values.append(config.box_type_weights.get('space_warp', 3))
    values.append(1 if config.box_float_display else 0)
    values.append(config.box_float_precision)

    # 空间错位
    values.append(config.warp_intensity)
    values.append(config.warp_segments)
    values.append(config.warp_glitch_chance)
    values.append(config.warp_shift_range[0])  # warp_shift_min
    values.append(config.warp_shift_range[1])  # warp_shift_max
    values.append(1 if config.warp_color_shift else 0)
    values.append(1 if config.warp_scanline_jitter else 0)

    # 噪声效果
    values.append(1 if config.enable_noise else 0)
    values.append(config.noise_perlin_scale)
    values.append(config.noise_perlin_octaves)
    values.append(config.noise_perlin_intensity)
    values.append(1 if config.noise_rgb_separate else 0)
    values.append(config.noise_rgb_r_intensity)
    values.append(config.noise_rgb_g_intensity)
    values.append(config.noise_rgb_b_intensity)
    values.append(1 if config.noise_scanline_enabled else 0)
    values.append(config.noise_scanline_intensity)
    values.append(config.noise_scanline_frequency)
    values.append(config.noise_strength)

    # 文字配置
    values.append(config.title_erosion_rate)
    values.append(config.node_text_chance)
    values.append(config.hud_line_chance)
    values.append(config.log_blocks_range[0])  # log_blocks_min
    values.append(config.log_blocks_range[1])  # log_blocks_max

    # 景深配置
    values.append(1 if config.enable_depth_of_field else 0)
    values.append(config.depth_blur_amount)
    values.append(config.depth_darken_amount)
    values.append(config.depth_focus_radius)
    values.append(config.depth_fade_start)

    # 错误配置
    values.append(1 if config.use_extended_errors else 0)

    return values


def update_config_from_input(config: CyberConfig, input_name: str, input_value) -> CyberConfig:
    """从UI输入更新配置"""

    # 颜色值处理
    if input_name.startswith('color_') or input_name == 'mesh_color' or input_name == 'box_line_color':
        # 从十六进制转换为RGBA元组
        rgba = hex_to_rgba(input_value)
        setattr(config, input_name, rgba)

    # 框数量范围
    elif input_name == 'box_count_min':
        config.box_count = (int(input_value), config.box_count[1])
    elif input_name == 'box_count_max':
        config.box_count = (config.box_count[0], int(input_value))

    # 框大小范围
    elif input_name == 'box_size_min':
        config.box_size_range = (int(input_value), config.box_size_range[1])
    elif input_name == 'box_size_max':
        config.box_size_range = (config.box_size_range[0], int(input_value))

    # 框类型权重
    elif input_name == 'box_type_plain':
        config.box_type_weights['plain'] = int(input_value)
    elif input_name == 'box_type_invert':
        config.box_type_weights['invert'] = int(input_value)
    elif input_name == 'box_type_bios':
        config.box_type_weights['bios'] = int(input_value)
    elif input_name == 'box_type_space_warp':
        config.box_type_weights['space_warp'] = int(input_value)

    # 错位偏移范围
    elif input_name == 'warp_shift_min':
        config.warp_shift_range = (int(input_value), config.warp_shift_range[1])
    elif input_name == 'warp_shift_max':
        config.warp_shift_range = (config.warp_shift_range[0], int(input_value))

    # 文字块范围
    elif input_name == 'log_blocks_min':
        config.log_blocks_range = (int(input_value), config.log_blocks_range[1])
    elif input_name == 'log_blocks_max':
        config.log_blocks_range = (config.log_blocks_range[0], int(input_value))

    # 复选框处理
    elif input_name in ['box_float_display', 'warp_color_shift', 'warp_scanline_jitter',
                        'enable_depth_of_field', 'use_extended_errors',
                        'enable_noise', 'noise_rgb_separate', 'noise_scanline_enabled']:
        setattr(config, input_name, bool(input_value))

    # 其他直接映射的属性
    else:
        # 检查属性是否存在
        if hasattr(config, input_name):
            # 根据值的类型设置
            current_value = getattr(config, input_name)
            if isinstance(current_value, float):
                setattr(config, input_name, float(input_value))
            elif isinstance(current_value, int):
                setattr(config, input_name, int(input_value))
            elif isinstance(current_value, bool):
                setattr(config, input_name, bool(input_value))
            else:
                setattr(config, input_name, input_value)

    return config