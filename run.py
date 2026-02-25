# run.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


def create_directories():
    """创建所有必要的目录"""
    directories = [
        "inputs",
        "outputs",
        "outputs/single",
        "outputs/batch",
        "configs",
        "static",
        "static/examples",
        "static/css"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 创建/确认目录: {directory}")

    # 创建示例图片（如果没有）
    example1_path = "static/examples/example1.jpg"
    example2_path = "static/examples/example2.jpg"

    if not os.path.exists(example1_path) or not os.path.exists(example2_path):
        create_example_images()


def create_example_images():
    """创建示例图片"""
    try:
        from PIL import Image, ImageDraw

        # 创建第一个示例图片
        img1 = Image.new('RGB', (800, 600), color=(40, 40, 60))
        draw1 = ImageDraw.Draw(img1)
        draw1.rectangle([100, 100, 700, 500], outline=(100, 200, 255), width=3)
        draw1.text((350, 280), "EXAMPLE 1", fill=(255, 255, 255))
        img1.save("static/examples/example1.jpg")

        # 创建第二个示例图片
        img2 = Image.new('RGB', (800, 600), color=(60, 40, 40))
        draw2 = ImageDraw.Draw(img2)
        draw2.ellipse([200, 150, 600, 450], outline=(255, 100, 100), width=3)
        draw2.text((350, 280), "EXAMPLE 2", fill=(255, 255, 255))
        img2.save("static/examples/example2.jpg")

        print("✅ 创建示例图片")
    except Exception as e:
        print(f"⚠️ 无法创建示例图片: {e}")


def check_dependencies():
    """检查依赖是否安装"""
    required_packages = ['gradio', 'opencv-python', 'numpy', 'Pillow']
    missing = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)

    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        return False

    print("✅ 所有依赖已安装")
    return True


def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ 依赖安装完成")


def main():
    print("=" * 50)
    print("🌆 赛博朋克图像生成器 - 启动脚本")
    print("=" * 50)

    # 创建目录
    create_directories()

    # 检查依赖
    if not check_dependencies():
        response = input("是否自动安装依赖？(y/n): ")
        if response.lower() == 'y':
            install_dependencies()
        else:
            print("请手动安装依赖后重试")
            return

    # 启动应用
    print("\n🚀 启动 Gradio 应用...")
    print("🌐 访问地址: http://localhost:7860")
    print("=" * 50)

    # 导入并运行主应用
    from app import demo
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        theme=gr.themes.Soft()
    )


if __name__ == "__main__":
    # 注意：需要在函数内部导入 gr，因为 theme 参数需要
    import gradio as gr

    main()