""" グローバルコンフィグのモデル

Attributes:
    config (Dict): Config dictionary
        Dict:
            "blog_title": string
            "copylight_name": string
            "copylight_url": string
            "issues_page_url": string (url of issue page)
            "favicon_image_url": string (url of favicon image)

            <Optional>
            "author_name": string
            "author_description": string
            "avatar_image_url": {"url": string, "path": string}
            "sns": {"name": string (e.g. "GitHub"), "url": string}
"""
import os
import json
from urllib.parse import urlparse

from functions.utils import color
from functions.images import dl_save_image, dl_image

class Config():
    def __init__(self, config={}, consts=None):
        positional_args = [
            'blog_title', 
            'copylight_name', 
            'copylight_url', 
            'issues_page_url',
            'favicon_image_url',
            ]
        for arg in positional_args:
            assert arg in config.keys(), f"Config needs '{arg}' field."
        assert consts is not None, "Config needs 'consts' arg."

        self.consts = consts
        self.config = config

    @classmethod
    def load(cls, consts):
        config_path = f"{consts.ETC_DIR}/config.json"
        if not os.path.exists(config_path):
            return None
        with open(config_path, 'r') as f:
            config = json.load(f)
        return Config(config, consts)

    @classmethod
    def from_issue(cls, issue, consts):
        fm = issue.fm
        assert fm is not None, "Issue needs yaml frontmatter."
        config = {}
        for key in fm.keys():
            config[key] = fm[key]

        assert 'root_url' in config.keys(), "Config needs 'root_url' field."
        config['root_url'] = config['root_url'][:-1] if config['root_url'][-1]=='/' else config['root_url']
        parsed = urlparse(config['root_url'])
        config['url_domain'] = parsed.netloc
        config['url_subpath'] = parsed.path

        return Config(config, consts)

    def save(self):
        self._save_favicon()
        self._save_avatar()
        self._save_consts_js()
        self._save_config_json()

    def _save_config_json(self):
        """ config.jsonを更新 """
        ETC_DIR = self.consts.ETC_DIR
        if not os.path.exists(ETC_DIR):
            os.makedirs(ETC_DIR)
        with open(f'{ETC_DIR}/config.json', 'w', encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        
    def _save_consts_js(self):
        """ lib/consts.jsを更新する """
        NEXTJS_BASE_PATH = self.consts.NEXTJS_BASE_PATH
        root_path = self.config.pop('root_url')
        base_path = self.config.pop('url_subpath')
        domain_path = self.config.pop('url_domain')
        if os.path.exists(f'{NEXTJS_BASE_PATH}/lib/consts.js'):
            with open(f"{NEXTJS_BASE_PATH}/lib/consts.js", 'r') as f:
                config = f.read().split('\n')
            for i, conf in enumerate(config):
                conf = conf.replace(' ', '')
                if "exports.rootPath=" in conf:
                    config[i] = f'exports.rootPath = "{root_path}"'
                if "exports.basePath=" in conf:
                    config[i] = f'exports.basePath = "{base_path}"'
                if "exports.domainPath=" in conf:
                    config[i] = f'exports.domainPath = "{domain_path}"'
        else:
            config = [
                    f'exports.rootPath = "{root_path}"',
                    f'exports.basePath = "{base_path}"',
                    f'exports.domainPath = "{domain_path}"',
                ]
        config = '\n'.join(config)
        if not os.path.exists(f'{NEXTJS_BASE_PATH}/lib'):
            os.makedirs(f'{NEXTJS_BASE_PATH}/lib')
        with open(f"{NEXTJS_BASE_PATH}/lib/consts.js", 'w') as f:
            f.write(config)

    def _save_favicon(self):
        if 'favicon_image_url' in self.config:
            image_url = self.config['favicon_image_url']
            img = dl_image(image_url)
            if img is not None:
                sizes = [(16,16), (32, 32), (48, 48), (64,64)]
                save_path = f'{self.consts.IMAGES_DIR}/favicon.ico'
                if not os.path.exists(self.consts.IMAGES_DIR):
                    os.makedirs(self.consts.IMAGES_DIR)
                img.save(save_path, sizes=sizes)

    def _save_avatar(self):
        if 'avatar_image_url' in self.config:
            image_url = self.config['avatar_image_url']
            image_url = dl_save_image(
                url=image_url,
                save_dir=self.consts.CONFIG_IMAGES_DIR,
                save_dir_prd=self.consts.CONFIG_IMAGES_DIR_PRD,
                file_name='avatar',
                extension='webp',
                max_image_width=600,
            )
            self.config['avatar_image_url'] = image_url

    def __getitem__(self, key):
        if key not in self.config.keys():
            return None
        return self.config[key]

    def keys(self):
        return self.config.keys()

    def __repr__(self):
        return ""


    def __str__(self):
        text = []
        for key in self.config.keys():
            text += [color('config.'+key, 'CYAN')+' = '+color(self.config[key], 'BROWN')]
        return "\n".join(text)

