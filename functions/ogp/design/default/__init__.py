""" OGP画像の生成

Returns:
    PIL image object
"""

from PIL import Image, ImageDraw, ImageFont

from functions.ogp.design.common.abstract import AbstractDesign
from functions.ogp.design.common import paste_icon_image, add_centered_text, add_lefted_text, is_text_size_ok
from functions.utils import import_module_with_install
tokenize = import_module_with_install(f'functions.related.models.default').tokenize

class Design(AbstractDesign):
    def __init__(self, issue, article, config, consts, thumbnail_image=None):
        self.thumbnail_image = thumbnail_image

        """ font """
        self.font_black_path = f"{self.COMMON_FONTS_DIR}/NotoSansJP-Black.otf"
        self.font_medium_path = f"{self.COMMON_FONTS_DIR}/NotoSansJP-Medium.otf"

        """ icon settings """
        self.icon_w = 60
        self.icon_h = 60
        self.icon_pos_h = 510
        self.icon_pos_w = 125

        """ title settings """
        self.side_padding = 250
        self.text_pos_h = 200
        self.title_font_size = 64
        self.title_margin_h = 50
        self.title_texts = tokenize(article.title)

        """ author settings """
        self.author_pos_h = 508
        self.author_pos_w = 200
        self.author_font_size = 42

        self.ogp_base_img_path = f'{self.COMMON_TEMPLATES_DIR}/default.png'
        try:
            self.ogp_icon_img_path = consts.PUBLIC_DIR+config['avatar_image_url']['path']
        except:
            self.ogp_icon_img_path = None

        self.author_text = config['author_name']

    def create(self):
        if self.thumbnail_image is None:
            base_img = Image.open(self.ogp_base_img_path).copy()
        else:
            base_img = self.thumbnail_image

        if self.ogp_icon_img_path is not None:
            icon_img = Image.open(self.ogp_icon_img_path).copy()
            base_img = paste_icon_image(
                    base_img, 
                    icon_img, 
                    self.icon_w, 
                    self.icon_h, 
                    self.icon_pos_h,
                    icon_pos_w = self.icon_pos_w,
                )

        draw = ImageDraw.Draw(base_img)
        font = ImageFont.truetype(self.font_black_path, self.title_font_size)
        text = self.title_texts[0]
        multiline = False
        for i, title_text in enumerate(self.title_texts[1:]):
            if is_text_size_ok(draw, font, text+title_text, base_img.size[0], self.side_padding, text_padding=250):
                text += title_text
            else:
                base_img = add_centered_text(
                        base_img, 
                        text,
                        self.font_black_path, 
                        self.title_font_size, 
                        (64, 64, 64), 
                        self.text_pos_h, 
                        self.side_padding,
                    )
                text = ''.join(self.title_texts[i:])
                self.text_pos_h += self.title_font_size
                multiline = True
                break
        self.text_pos_h = self.text_pos_h + self.title_margin_h if multiline else self.text_pos_h + self.title_margin_h//2
        base_img = add_centered_text(
                base_img, 
                text,
                self.font_black_path, 
                self.title_font_size, 
                (64, 64, 64), 
                self.text_pos_h, 
                self.side_padding,
            )

        base_img = add_lefted_text(
                base_img, 
                self.author_text, 
                self.font_medium_path, 
                self.author_font_size, 
                (120, 120, 120), 
                (self.author_pos_w, self.author_pos_h), 
                self.side_padding,
            )
        return base_img

