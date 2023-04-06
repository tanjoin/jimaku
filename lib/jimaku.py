import importlib
import math
from PIL import Image, ImageDraw
from lib.font_config import FontConfig

# ファイルから字幕をつける
def puts(src, text_file, font_config = FontConfig(), output = 'dst/'):
    img = Image.open(src)

    file = open(text_file, 'r')
    lines = file.readlines()

    count = 0
    for line in lines:
        count += 1
        _draw_text(img.copy(), output + str(count).zfill(3) + ".png", line, font_config)

# 字幕をつける
def put(src, text, font_config = FontConfig(), output = 'dst/'):
    img = Image.open(src)
    _draw_text(img, output + "output.png", text, font_config)

# 画像に描画して保存する
def _draw_text(img, filename, text, font_config = FontConfig()):
    w, h = img.size
    w5 = int(w * 0.5)
    h9 = int(h * 0.9)
    tx, ty = font_config.get_text_dimensions(text)

    xx = int(w5 - (tx / 2))

    for i in range(0, 360, 5):
        pos_xr = font_config.font_width * math.cos(2 * 3.14 * i / 360)
        pos_yr = font_config.font_width * math.sin(2 * 3.14 * i / 360)
        ImageDraw.Draw(img).text((xx + pos_xr, h9 + pos_yr), text, font = font_config.font, fill = font_config.back_color)

    ImageDraw.Draw(img).text((xx, h9), text, font = font_config.font, fill = font_config.font_color)
    img.save(filename, quality=100)
