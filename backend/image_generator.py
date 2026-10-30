# -*- coding: utf-8 -*-
"""书法作品图生成器

根据作品信息动态生成 SVG 书法作品图，无需外部图片资源。
支持缩略图（thumbnail）与高清大图（large）两种尺寸，用于
传世之作列表与作品详情页展示。

风格：宣纸底色 + 竖排/横排书法字 + 朱砂印章 + 宫廷色边框装饰。
"""

from xml.sax.saxutils import escape


# 书体对应的主色调（与前端风格保持一致）
STYLE_COLORS = {
    "小篆": "#b0693a",
    "篆书": "#b0693a",
    "隶书": "#2b4a6f",
    "楷书": "#c3272b",
    "行书": "#5fa383",
    "行楷": "#5fa383",
    "行草": "#7fb89a",
    "草书": "#d4a017",
    "狂草": "#d4a017",
    "标准草书": "#d4a017",
    "六分半书": "#b0693a",
}


def _color(style):
    return STYLE_COLORS.get(style, "#c3272b")


def _clamp_font_size(length, base, max_size, min_size):
    """根据文字长度自适应字号"""
    if length <= 1:
        return max_size
    size = base / length
    return max(min_size, min(max_size, size))


def generate_work_svg(work, size="large"):
    """生成书法作品 SVG 图

    :param work: 作品字典，需包含 name, style, calligrapher_name, dynasty_name
    :param size: "thumbnail" 或 "large"
    :return: SVG 字符串
    """
    name = work.get("name", "佚名")
    style = work.get("style", "")
    author = work.get("calligrapher_name", "")
    dynasty = work.get("dynasty_name", "")
    color = _color(style)

    if size == "thumbnail":
        return _render_thumbnail(name, style, author, color)
    return _render_large(name, style, author, dynasty, color)


def _render_thumbnail(name, style, author, color):
    """缩略图：横向构图，宣纸底 + 横排作品名 + 印章 + 书体标签"""
    width, height = 400, 300
    # 横排作品名，自适应字号
    display = name if len(name) <= 6 else name[:6]
    font_size = _clamp_font_size(len(display), 320, 64, 34)

    # 印章文字（作者姓）
    seal_char = escape(author[:1]) if author else "书"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="paper" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#faf6ef"/>
      <stop offset="100%" stop-color="#f3ebdd"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#paper)"/>
  <!-- 装饰边框 -->
  <rect x="14" y="14" width="{width-28}" height="{height-28}" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.55"/>
  <rect x="20" y="20" width="{width-40}" height="{height-40}" fill="none" stroke="{color}" stroke-width="0.6" opacity="0.35"/>
  <!-- 书体标签 -->
  <text x="34" y="46" font-family="Songti SC, STSong, SimSun, serif" font-size="15" fill="{color}" letter-spacing="3" opacity="0.8">{escape(style)}</text>
  <!-- 作品名 -->
  <text x="{width/2}" y="{height/2 + font_size/3}" font-family="Songti SC, STSong, SimSun, serif" font-size="{font_size}" font-weight="700" fill="#3a3a3a" text-anchor="middle">{escape(display)}</text>
  <!-- 朱砂印章 -->
  <rect x="{width-66}" y="{height-66}" width="40" height="40" fill="#c3272b" rx="3"/>
  <text x="{width-46}" y="{height-40}" font-family="Songti SC, STSong, SimSun, serif" font-size="20" font-weight="700" fill="#faf6ef" text-anchor="middle">{seal_char}</text>
</svg>"""
    return svg


def _render_large(name, style, author, dynasty, color):
    """高清大图：竖轴构图，宣纸底 + 竖排作品名 + 印章 + 朝代书体 + 装饰"""
    width, height = 800, 1000
    # 竖排显示，最多前 8 字
    display = name if len(name) <= 8 else name[:8]
    char_count = len(display)
    font_size = _clamp_font_size(char_count, 720, 96, 60)
    line_height = font_size * 1.35
    # 竖排起始 y
    start_y = (height - line_height * char_count) / 2 + font_size

    seal_char = escape(author[:1]) if author else "书"

    # 逐字定位（竖排居中）
    chars_svg = ""
    for i, ch in enumerate(display):
        y = start_y + i * line_height
        chars_svg += f'\n  <text x="{width/2}" y="{y}" font-family="Songti SC, STSong, SimSun, serif" font-size="{font_size}" font-weight="700" fill="#2c2c2c" text-anchor="middle">{escape(ch)}</text>'

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="paper" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#faf6ef"/>
      <stop offset="100%" stop-color="#f1e8d6"/>
    </linearGradient>
    <linearGradient id="sealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c3272b"/>
      <stop offset="100%" stop-color="#a01f23"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#paper)"/>
  <!-- 外层装饰边框 -->
  <rect x="30" y="30" width="{width-60}" height="{height-60}" fill="none" stroke="{color}" stroke-width="2" opacity="0.5"/>
  <rect x="40" y="40" width="{width-80}" height="{height-80}" fill="none" stroke="{color}" stroke-width="0.8" opacity="0.35"/>
  <!-- 顶部标题区 -->
  <text x="{width/2}" y="92" font-family="Songti SC, STSong, SimSun, serif" font-size="26" fill="{color}" text-anchor="middle" letter-spacing="6" opacity="0.85">{escape(style)}</text>
  <line x1="120" y1="112" x2="{width-120}" y2="112" stroke="{color}" stroke-width="0.8" opacity="0.4"/>
  <!-- 竖排作品名 -->
  {chars_svg}
  <!-- 底部朝代落款 -->
  <text x="{width/2}" y="{height-110}" font-family="Songti SC, STSong, SimSun, serif" font-size="22" fill="#6b5d4a" text-anchor="middle" letter-spacing="4" opacity="0.8">{escape(dynasty)} · {escape(author)}</text>
  <!-- 朱砂印章 -->
  <rect x="{width/2-34}" y="{height-90}" width="68" height="68" fill="url(#sealGrad)" rx="4"/>
  <text x="{width/2}" y="{height-44}" font-family="Songti SC, STSong, SimSun, serif" font-size="34" font-weight="700" fill="#faf6ef" text-anchor="middle">{seal_char}</text>
</svg>"""
    return svg
