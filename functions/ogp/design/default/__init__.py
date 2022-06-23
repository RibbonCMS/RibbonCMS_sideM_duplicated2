""" OGP画像の生成

Returns:
    PIL image object
"""

from PIL import Image

from functions.ogp.design.common.abstract import AbstractDesign
from functions.ogp.design.common import paste_icon_image, add_centered_text

class Design(AbstractDesign):
    def __init__(self, issue, article, config, consts):
        """ font """
        self.font_black_path = f"{self.COMMON_FONTS_DIR}/NotoSansJP-Black.otf"
        self.font_medium_path = f"{self.COMMON_FONTS_DIR}/NotoSansJP-Medium.otf"

        """ icon settings """
        self.icon_w = 150
        self.icon_h = 150
        self.icon_pos_h = 220

        """ title settings """
        self.side_padding = 550
        self.text_pos_h = 400
        self.title_font_size = 72

        """ author settings """
        self.author_pos_h = 620
        self.author_font_size = 42

        self.ogp_base_img_path = f'{self.COMMON_TEMPLATES_DIR}/default.png'
        try:
            self.ogp_icon_img_path = consts.PUBLIC_DIR+config['avatar_image_url']['path']
        except:
            self.ogp_icon_img_path = None
        self.title_text = article.title
        self.author_text = config['author_name']

    def create(self):
        base_img = Image.open(self.ogp_base_img_path).copy()

        if self.ogp_icon_img_path is not None:
            icon_img = Image.open(self.ogp_icon_img_path).copy()
            base_img = paste_icon_image(
                    base_img, 
                    icon_img, 
                    self.icon_w, 
                    self.icon_h, 
                    self.icon_pos_h,
                )

        base_img = add_centered_text(
                base_img, 
                self.title_text, 
                self.font_black_path, 
                self.title_font_size, 
                (64, 64, 64), 
                self.text_pos_h, 
                self.side_padding,
            )
        base_img = add_centered_text(
                base_img, 
                self.author_text, 
                self.font_medium_path, 
                self.author_font_size, 
                (120, 120, 120), 
                self.author_pos_h, 
                self.side_padding,
            )
        return base_img

