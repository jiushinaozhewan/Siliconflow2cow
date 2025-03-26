# Siliconflow2cowPlus 插件  (包含免费的kolors模型)

这是一个基于 Siliconflow2cow 的增强版图像生成插件，支持通过简单的命令生成高质量图片。

## 功能特点

- 支持多种绘图命令前缀（"绘"、"draw"）
- 支持多种图片比例（1:1）
- 自动清理过期图片
- 支持自定义配置

 ## 安装方法

1. #installp https://github.com/jiushinaozhewan/Siliconflow2cow.git
2. #scanp
3. 配置config.json

## 使用方法

1. 在配置文件中设置你的认证令牌（auth_token）
2. 使用以下命令格式生成图片：
   - `绘 一只可爱的猫 -m kolors ---16:9`
   - `draw a cute cat`

## 配置说明

配置文件 `config.json` 包含以下选项：

- `auth_token`: 认证令牌
- `drawing_prefixes`: 绘图命令前缀列表
- `image_output_dir`: 图片输出目录
- `clean_interval`: 图片清理间隔（小时）
- `clean_check_interval`: 清理检查间隔（秒）
- `supported_models`: 支持的模型列表
- `aspect_ratios`: 支持的图片比例

## 注意事项

- 请确保配置文件中的认证令牌有效
- 图片会自动保存在配置的输出目录中
- 过期图片会自动清理 
