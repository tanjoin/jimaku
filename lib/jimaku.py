from PIL import Image, ImageDraw, ImageFont
import math

# 字幕を設置する
def put(src, text, font_size = 64, font = '/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc', font_color = (255, 255, 255), back_color = (15, 128, 255), font_width = 10):
    img = Image.open(src)
    w, h = img.size
    w5 = int(w * 0.5)
    h8 = int(h * 0.9)
    print('width: ', w, '80%: ', w5)
    print('height; ', h, '80%: ', h8)

    font = ImageFont.truetype(font, font_size)

    tx, ty = get_text_dimensions(text, font)
    print('text width: ', tx)
    print('text height: ', ty)

    xx = int(w5 - (tx / 2))

    for i in range(0, 360, 5):
        pos_xr = font_width * math.cos(2 * 3.14 * i / 360)
        pos_yr = font_width * math.sin(2 * 3.14 * i / 360)
        ImageDraw.Draw(img).text((xx + pos_xr, h8 + pos_yr), text, font = font, fill = back_color)
    ImageDraw.Draw(img).text((xx, h8), text, font = font, fill = font_color)
    img.save('add_text.png', quality=100)

# テキストのサイズを取得する
def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)