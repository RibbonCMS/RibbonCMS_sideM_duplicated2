""" OGP画像の生成

`functions/ogp/design/*.py`からデザインを選択して画像を生成する．

Args:
    params:
        title: string
        slug: string
        author_name: string
        url_domain: string:
        avatar_image_url: string
        thumbnail_theme: string
        thumbnail_image_url: string / None
    thumbnail_save_path: string

Output:
    `front/public/static/images/thumbnail/[slug].jpg`
"""

import os

from functions.utils import import_module_with_install
from functions.images import dl_image

def generate_ogp_image(issue, article, config, consts, thumbnail_save_path):
    theme = issue.get_fm('thumbnail_theme')
    thumbnail_image = dl_image(issue.get_fm('thumbnail_image_url'))
    
    try:
        design = import_module_with_install('functions.ogp.design.'+theme)
    except:
        design = import_module_with_install('functions.ogp.design.default')

    design = design.Design(issue, article, config, consts, thumbnail_image)
    img = design.create()

    img = format_thumbnail(img)
    save_dir = "/".join(thumbnail_save_path.split('/')[:-1])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    img.save(thumbnail_save_path)

def format_thumbnail(img):
    img = _crop_img(img)
    img = _resize_img(img)
    img = img.convert('RGB')
    return img

def _crop_img(img):
    """ 1.91:1になるようにクロップする """
    w, h = img.width, img.height
    crop_w = w
    crop_h = w / 1.92
    if h < crop_h:
        crop_w = h * 1.92
        crop_h = h
    return img.crop(((w - crop_w) // 2,
                     (h - crop_h) // 2,
                     (w + crop_w) // 2,
                     (h + crop_h) // 2))

def _resize_img(img):
    resize_w = 1200
    resize_h = 630
    w, h = img.width, img.height
    if resize_w > w or resize_h > h:
        resize_w = w
        resize_h = h
    img = img.resize((resize_w, resize_h))
    return img

