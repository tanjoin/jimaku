from PIL import ImageFont

class FontConfig:
    
    def __init__(self):
        self.back_color = ( 15, 128, 255)
        self.font_color = (255, 255, 255)
        self.font_path  = '/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc'
        self.font_size  = 64
        self.font_width = 10
        self.update()

    def update(self):
        self.font = ImageFont.truetype(self.font_path, self.font_size)

    # テキストのサイズを取得する
    def get_text_dimensions(self, text_string):
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = self.font.getmetrics()

        text_width = self.font.getmask(text_string).getbbox()[2]
        text_height = self.font.getmask(text_string).getbbox()[3] + descent

        return (text_width, text_height)