""" OGP画像デザインの抽象クラス

Returns:
    PIL image object
"""

from abc import ABC, abstractmethod

class AbstractDesign(ABC):
    DESIGN_DIR = f'./functions/ogp/design'
    COMMON_DIR = f'{DESIGN_DIR}/common'
    COMMON_FONTS_DIR = f'{COMMON_DIR}/fonts'
    COMMON_TEMPLATES_DIR = f'{COMMON_DIR}/templates'

    @abstractmethod
    def __init__(self, issue, article, config, consts, thumbnail_image=None):
        pass

    @abstractmethod
    def create(self):
        pass

