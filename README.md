
# AlgorithmGlitchCore

> 一个实验性的图像处理工具，通过算法生成的故障效果，创造出报错和图像拥抱的瞬间。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Gradio](https://img.shields.io/badge/gradio-5.9+-orange.svg)

## 🌌 项目理念
**在算法生成的世界中，我们是否可以通过错误来创造独特的美学体验？**

AlgorithmGlitchCore 诞生于对 AlgorithmHellYeahCore 与 Glitch Core 的探索，参考了部分Y2K美学、Dreamcore、Weirdcore 等数字艺术流派的视觉语言。

本项目是一个实验性的图像处理工具。

部分视觉灵感来源于《明日方舟》主线第十五章，试图通过数字故障的形式，呈现科技、理性与混沌的碰撞。

## ✨ 核心特性

### 🎨 多重故障效果
- **CRT 屏幕效果** - 模拟老式显示器的色彩偏移与扫描线
- **空间错位框** - 像素级别的扭曲与错位
- **景深效果** - 焦点区域的保留与边缘的模糊淡化
- **神经线网格** - 仿生学风格的连接线

### 🎮 高度可配置
- 4 种类型的框（普通、反色、BIOS、空间错位）
- 16+ 种错误消息类别（从内核 panic 到 ML 训练错误）
- 实时参数调整与预览
- 配置保存/加载功能

### 🖼️ 灵活的使用方式
- **单张处理** - 快速尝试不同效果
- **批量处理** - 批量生成风格一致的图片
- **实时预览** - 在调整参数时即时查看效果

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/AlgorithmGlitchCore.git
cd AlgorithmGlitchCore

# 安装依赖
pip install -r requirements.txt

# 创建必要的目录
python run.py
```

### 启动

```bash
# 方式1：直接启动
python app.py

# 方式2：使用启动脚本（自动检查环境）
python run.py
```

访问 `http://localhost:7860` 打开 Web 界面。

## 📖 使用指南

### 1. 单张处理
- 上传图片或点击示例图片
- 设置随机种子（-1 表示完全随机）
- 点击生成按钮
- 查看并下载结果

### 2. 批量处理
- 将图片放入 `inputs` 目录
- 指定种子列表（可选）
- 点击批量生成
- 结果保存在 `outputs/batch` 目录

### 3. 配置管理
- 在配置标签页调整所有参数
- 实时预览配置变化
- 保存常用配置模板
- 加载已保存的配置

## ⚙️ 参数详解

### 颜色配置
- **错误文字** - 红色系，突出系统错误信息
- **普通文字** - 白色，用于调试信息和日志
- **边框/连线** - 半透明白色，营造科技感

### 框类型
| 类型 | 权重   | 描述 |
|------|------|------|
| 普通框 | 3/10 | 基础边框，显示随机浮点数 |
| 反色框 | 2/10 | 区域内图像反色处理 |
| BIOS框 | 4/10 | 带标题栏的系统风格框 |
| 空间错位 | 3/10 | 区域内像素扭曲错位 |

### 错误消息
包含 15+ 个类别，超过 500 条错误消息：
- 💀 致命系统错误
- 🔐 哈希校验失败
- 🤖 机器学习错误
- 📚 堆栈跟踪
- 等等...

## 🎯 设计理念

本项目本来是做着随便玩玩的，但是意外发现效果不错，那就公开给大家看看了，希望能给喜欢赛博朋克、Y2K、Dreamcore、Weirdcore 等风格的朋友们带来一些灵感和乐趣。

互联网里找到点自己喜欢的东西也不容易，现在也是动不动就要花钱，所以就想做个免费的工具，给大家提供一些创作的可能性。

总而言之，这个项目是一个实验性的艺术工具，旨在通过算法生成的故障效果，探索数字美学的边界。无论你是艺术家、设计师还是开发者，都欢迎来尝试和贡献！ 🚀✨

## 📁 项目结构

```
AlgorithmGlitchCore/
│
├── configs/                          # 配置文件保存目录
│   └── (自动生成的配置JSON文件)
│
├── core/                              # 核心渲染引擎
│   ├── __init__.py                    # 模块初始化，导出核心函数
│   ├── boxes.py                        # 框绘制逻辑（普通框、反色框、BIOS框、空间错位框）
│   ├── effects.py                       # 特效处理（CRT效果、景深效果、空间错位）
│   ├── renderer.py                      # 主渲染器（核心处理流程）
│   ├── text.py                          # 文字绘制（错误消息、调试信息）
│   └── utils.py                         # 工具函数（主体检测、网格绘制、神经线）
│
├── data/                              # 数据文件
│   ├── __init__.py                     # 模块初始化
│   └── error_messages.py                # 错误消息字典
│
├── outputs/                           # 输出目录
│   └── single/                         # 单张处理输出
│       └── (生成的图片文件)
│
├── static/                            # 静态资源
│   ├── css/                            # 样式文件
│   │   └── style.css                    # 自定义CSS样式
│   └── examples/                        # 示例图片
│       ├── example1.jpg
│       └── example2.jpg
│
├── ui/                                # 用户界面模块
│   ├── components/                      # UI组件
│   │   ├── __init__.py
│   │   ├── color_picker.py               # 颜色选择器组件
│   │   └── slider_group.py               # 滑块组组件
│   ├── tabs/                            # 标签页
│   │   ├── __init__.py
│   │   ├── batch.py                       # 批量处理标签页
│   │   ├── config.py                      # 配置管理标签页
│   │   ├── preview.py                     # 效果预览标签页
│   │   └── single.py                      # 单张处理标签页
│   ├── __init__.py
│   └── utils.py                          # UI工具函数（颜色转换、配置管理）
│
├── app.py                              # Gradio Web应用主入口（模块化版本）
├── config.py                           # 配置类定义（CyberConfig）                          
└── run.py                              # 启动脚本（自动创建目录、检查依赖）
```
## 示例图片

![example1](static/pics/example1.jpg)
**暖调的大桥**

![example2](static/pics/example2.jpg)
**灰调的电视塔**

## TODO

### 随机噪声效果
- [ ] Perlin噪声 - 模拟胶片颗粒和自然纹理
- [ ] RGB通道独立噪声 - 三个颜色通道分别添加不同程度的噪声
- [ ] 扫描线噪声 - 模拟老式电视的扫描线干扰
- [ ] 噪声强度滑块 - 可调节的噪声强度控制

### 视频处理支持
- [ ] 视频帧提取 - 从视频中提取帧序列
- [ ] 批量帧处理 - 对每一帧应用故障效果
- [ ] 帧连续性优化 - 确保相邻帧之间的效果过渡自然
- [ ] 视频合成 - 将处理后的帧重新合成为视频

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！无论是新功能建议、bug 修复还是新的错误消息，都欢迎参与。

### 开发建议
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢 Algorithm HellYeahCore 与 Glitch Core 的启发
- 感谢《明日方舟》主线第十五章提供的视觉灵感
- 感谢所有 Y2K、Dreamcore、Weirdcore 创作者

---

**在算法的裂缝中，我们寻找着美的另一种可能。** 🌃
