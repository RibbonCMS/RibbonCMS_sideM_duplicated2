""" ディレクトリパスなどの定数

Args:
    test_dir (None / string): None => 本番用定数をセット
                              string => `test_dir`用定数をセット
    skip_download (bool): 開発時にダウンロード処理をスキップできるように

Params: 
    Labels:
        ARTICLE_FLAG_LABEL : string
        DELETE_FLAG_LABEL : string
        CONFIG_FLAG_LABEL : string
        FIXED_FLAG_LABEL : string
        EXEC_WORKFLOW_FLAG_LABELS : string[]

    SideF path:
        IMAGES_DIR_PRD : string
        ARTICLE_IMAGES_DIR_PRD : string
        EXTERNAL_IMAGES_DIR_PRD : string
        THUMBNAIL_IMAGES_DIR_PRD : string
        FIXED_IMAGES_DIR_PRD : string
        CONFIG_IMAGES_DIR_PRD : string

    SideM path:
        ISSUE_PATH : string
        NEXTJS_BASE_PATH : string
        CONTENTS_DIR : string
        PUBLIC_DIR : string
        MD_DIR : string
        ETC_DIR : string
        FIXED_DIR : string
        IMAGES_DIR : string
        ARTICLE_IMAGES_DIR : string
        EXTERNAL_IMAGES_DIR_PRD
        THUMBNAIL_IMAGES_DIR : string
        FIXED_IMAGES_DIR : string
        CONFIG_IMAGES_DIR : string

    Other:
        MAX_IMAGE_WIDTH : int
        THUMBNAIL_EXTENSION : string
        test_dir: None / string
        skip_download : bool
"""

import os

from functions.utils import color

class Consts():
    """ Issue Label """
    ARTICLE_FLAG_LABEL = 'article'
    DELETE_FLAG_LABEL = 'delete'
    CONFIG_FLAG_LABEL = 'config'
    FIXED_FLAG_LABEL = 'fixed'

    """ workflowが動作するラベル """
    EXEC_WORKFLOW_FLAG_LABELS = [
        ARTICLE_FLAG_LABEL, 
        DELETE_FLAG_LABEL,
        CONFIG_FLAG_LABEL,
        FIXED_FLAG_LABEL,
        ]
    
    """ フロント側のstaticパス """
    IMAGES_DIR_PRD = f'/static/images'
    ARTICLE_IMAGES_DIR_PRD = f'{IMAGES_DIR_PRD}/articles'
    EXTERNAL_IMAGES_DIR_PRD = f'{IMAGES_DIR_PRD}/external_ogp'
    THUMBNAIL_IMAGES_DIR_PRD = f'{IMAGES_DIR_PRD}/thumbnail'
    FIXED_IMAGES_DIR_PRD = f'{IMAGES_DIR_PRD}/fixed'
    CONFIG_IMAGES_DIR_PRD = f'{IMAGES_DIR_PRD}/config'

    MAX_IMAGE_WIDTH = 550
    THUMBNAIL_EXTENSION = 'jpg'

    def __init__(self, test_dir=None, skip_download=False):
        self.test_dir = test_dir
        self.skip_download = skip_download

        if test_dir is not None:
            self._set_path(f'./tests/{test_dir}')
        else:
            self._set_path('..')
        assert os.path.exists(self.ISSUE_PATH), f"Directory not found; {self.ISSUE_PATH}"

    def _set_path(self, root_dir):
        self.ISSUE_PATH = f'{root_dir}/issue'
        self.NEXTJS_BASE_PATH = f'{root_dir}/front_contents'
        self.NEXTJS_FRONTEND_BASE_PATH = f'{root_dir}/front/src'

        self.CONTENTS_DIR = f'{self.NEXTJS_BASE_PATH}/contents'
        self.PUBLIC_DIR = f'{self.NEXTJS_BASE_PATH}/public'

        self.MD_DIR = f'{self.CONTENTS_DIR}/articles'
        self.ETC_DIR = f'{self.CONTENTS_DIR}/etc'
        self.FIXED_DIR = f'{self.CONTENTS_DIR}/fixed'

        self.IMAGES_DIR = f'{self.PUBLIC_DIR}{self.IMAGES_DIR_PRD}'
        self.ARTICLE_IMAGES_DIR = f'{self.PUBLIC_DIR}{self.ARTICLE_IMAGES_DIR_PRD}'
        self.EXTERNAL_IMAGES_DIR = f'{self.PUBLIC_DIR}{self.EXTERNAL_IMAGES_DIR_PRD}'
        self.THUMBNAIL_IMAGES_DIR = f'{self.PUBLIC_DIR}{self.THUMBNAIL_IMAGES_DIR_PRD}'
        self.FIXED_IMAGES_DIR = f'{self.PUBLIC_DIR}{self.FIXED_IMAGES_DIR_PRD}'
        self.CONFIG_IMAGES_DIR = f'{self.PUBLIC_DIR}{self.CONFIG_IMAGES_DIR_PRD}'

    def __repr__(self):
        return f'Consts(test_dir="{self.test_dir}")'

    def __str__(self):
        def color_params(line):
            line = line.split(' = ')
            line[0] = color(line[0], 'CYAN')
            line[1] = color(line[1], 'BROWN')
            return f'{line[0]} = {line[1]}'
        string = []
        string += [f'Issue Labels:']
        string += [color_params(f'  ARTICLE_FLAG_LABEL = "{self.ARTICLE_FLAG_LABEL}"')]
        string += [color_params(f'  DELETE_FLAG_LABEL = "{self.DELETE_FLAG_LABEL}"')]
        string += [color_params(f'  CONFIG_FLAG_LABEL = "{self.CONFIG_FLAG_LABEL}"')]
        string += [color_params(f'  FIXED_FLAG_LABEL = "{self.FIXED_FLAG_LABEL}"')]
        string += [color_params(f'  EXEC_WORKFLOW_FLAG_LABELS = {self.EXEC_WORKFLOW_FLAG_LABELS}')]

        string += [f'\nPath (sideF):']
        string += [color_params(f'  IMAGES_DIR_PRD = "{self.IMAGES_DIR_PRD}"')]
        string += [color_params(f'  ARTICLE_IMAGES_DIR_PRD = "{self.ARTICLE_IMAGES_DIR_PRD}"')]
        string += [color_params(f'  EXTERNAL_IMAGES_DIR_PRD = f"{self.EXTERNAL_IMAGES_DIR_PRD}"')]
        string += [color_params(f'  THUMBNAIL_IMAGES_DIR_PRD = "{self.THUMBNAIL_IMAGES_DIR_PRD}"')]
        string += [color_params(f'  FIXED_IMAGES_DIR_PRD = "{self.FIXED_IMAGES_DIR_PRD}"')]
        string += [color_params(f'  CONFIG_IMAGES_DIR_PRD = "{self.CONFIG_IMAGES_DIR_PRD}"')]

        string += [f'\nPath (sideM):']
        string += [color_params(f'  ISSUE_PATH = "{self.ISSUE_PATH}"')]
        string += [color_params(f'  NEXTJS_BASE_PATH = "{self.NEXTJS_BASE_PATH}"')]
        string += [color_params(f'  CONTENTS_DIR = "{self.CONTENTS_DIR}"')]
        string += [color_params(f'  PUBLIC_DIR = "{self.PUBLIC_DIR}"')]
        string += [color_params(f'  MD_DIR = "{self.MD_DIR}"')]
        string += [color_params(f'  ETC_DIR = "{self.ETC_DIR}"')]
        string += [color_params(f'  FIXED_DIR = "{self.FIXED_DIR}"')]
        string += [color_params(f'  IMAGES_DIR = "{self.IMAGES_DIR}"')]
        string += [color_params(f'  ARTICLE_IMAGES_DIR = "{self.ARTICLE_IMAGES_DIR}"')]
        string += [color_params(f'  EXTERNAL_IMAGES_DIR = f"{self.EXTERNAL_IMAGES_DIR}"')]
        string += [color_params(f'  THUMBNAIL_IMAGES_DIR = "{self.THUMBNAIL_IMAGES_DIR}"')]
        string += [color_params(f'  FIXED_IMAGES_DIR = "{self.FIXED_IMAGES_DIR}"')]
        string += [color_params(f'  CONFIG_IMAGES_DIR = "{self.CONFIG_IMAGES_DIR}"')]

        string += [f'\nOTHER:']
        string += [color_params(f'  MAX_IMAGE_WIDTH = {self.MAX_IMAGE_WIDTH}')]
        string += [color_params(f'  THUMBNAIL_EXTENSION = {self.THUMBNAIL_EXTENSION}')]
        string += [color_params(f'  test_dir = "{self.test_dir}"')]
        string += [color_params(f'  skip_download = {self.skip_download}')]

        return '\n'.join(string)
