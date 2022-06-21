""" fixedに関する処理．

dictの要素の解析等

Output:
    `front/contents/fixed/{fixed_name}.json`
    `front/public/static/images/fixed/{fixed_name}/[md5].webp`
    (optional) `front/public/static/images/fixed/{fixed_name}/thumbnail.jpg`
"""

import os
import json
import shutil

from functions.images import dl_save_image
from functions.utils import color

def _is_list(data):
    return type(data) is list

def _is_dict(data):
    return type(data) is dict

def _is_image_url(key, item):
    key = '_'.join(key.split('_')[-2:])
    is_image = key == 'image_url' and type(item) is str
    return is_image

class Fixed():
    def __init__(self, fixed, fixed_name, consts):
        self.fixed_name = fixed_name
        self.consts = consts
        self._clean_up_files()
        self.fixed = self._dig(fixed)

    def _clean_up_files(self):
        self._delete_images_fixed()
        
    def _delete_images_fixed(self):
        fixed_images_dir = f'{self.consts.FIXED_IMAGES_DIR}/{self.fixed_name}'
        if os.path.exists(fixed_images_dir):
            shutil.rmtree(fixed_images_dir)

    def _dig(self, element):
        if _is_list(element):
            return self._dig_list(element)
        elif _is_dict(element):
            return self._dig_dict(element)
        else:
            return element

    def _dig_list(self, element):
        return [self._dig(e) for e in element]

    def _dig_dict(self, element):
        for key in element.keys():
            e = element[key]
            e = self._key_action(key, e)
            element[key] = self._dig(e)
        return element

    def _key_action(self, key, item):
        if _is_image_url(key, item):
            return self._image_url_key_action(key, item)
        return item

    def _image_url_key_action(self, key, item):
        name = '_'.join(key.split('_')[:-2])
        fixed_images_dir = f'{self.consts.FIXED_IMAGES_DIR}/{self.fixed_name}'
        fixed_images_dir_prd = f'{self.consts.FIXED_IMAGES_DIR_PRD}/{self.fixed_name}'
        extension = 'webp'
        max_image_width = 1200
        if name == 'thumbnail':
            extension = 'jpg'
        else:
            name = None
        image_url = dl_save_image(
                url=item,
                save_dir=fixed_images_dir,
                save_dir_prd=fixed_images_dir_prd,
                file_name=name,
                extension=extension,
                max_image_width=max_image_width,
            )
        return image_url
    
    def __repr__(self):
        string  = f"Fixed(\n"
        string += f"    fixed={self.fixed},\n"
        string += f"    fixed_name={self.fixed_name},\n"
        string += f"    consts={repr(self.consts)},\n"
        string += f")"
        return string


    def __str__(self):
        fixed_name = color('fixed_name', 'CYAN') + ' = ' + color(f"'{self.fixed_name}'", "BROWN")
        fixed = color('fixed', 'CYAN') + ' = \n' + color(json.dumps(self.fixed, indent=4, ensure_ascii=False), "BROWN")
        return f"{fixed_name}\n{fixed}"

    def save(self):
        fixed_path = f'{self.consts.FIXED_DIR}/{self.fixed_name}.json'
        if not os.path.exists(self.consts.FIXED_DIR):
            os.makedirs(self.consts.FIXED_DIR)
        with open(fixed_path, 'w', encoding='utf-8') as f:
            json.dump(self.fixed, f, indent=4, ensure_ascii=False)

