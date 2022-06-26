""" OGP画像の生成

Returns:
    PIL image object
"""

from functions.ogp.design.common.abstract import AbstractDesign

class Design(AbstractDesign):
    def __init__(self, issue, article, config, consts, thumbnail_image):
        self.thumbnail_image = thumbnail_image

    def create(self):
        return self.thumbnail_image

