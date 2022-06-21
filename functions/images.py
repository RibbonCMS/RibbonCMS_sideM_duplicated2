""" 画像に関する処理．

画像DLやリサイズなど

Returns:
    PIL image object
"""
import io
import os
from PIL import Image
import urllib.request
import hashlib
import re

def dl_image(url):
    try:
        with urllib.request.urlopen(url) as web_file:
            img = io.BytesIO(web_file.read())
            img = Image.open(img)
        return img
    except:
        return None

def save_image(img, save_path):
    save_dir = '/'.join(save_path.split('/')[:-1])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    img.save(save_path)

def optimize_image_width(img, max_image_width):
    w, h = img.width, img.height
    if w > max_image_width:
        resize_ratio = w / max_image_width
        resized_w = int(w / resize_ratio)
        resized_h = int(h / resize_ratio)
        img = img.resize((resized_w, resized_h))
    return img

def dl_save_image(
            url, 
            save_dir, 
            save_dir_prd, 
            file_name=None,
            extension="webp",
            max_image_width=600,
        ):
    if file_name is None:
        file_name = hashlib.md5(url.encode()).hexdigest()
    file_name = f"{file_name}.{extension}"
    dst_path = f"{save_dir}/{file_name}"
    dst_prd_path = f"{save_dir_prd}/{file_name}"

    img = dl_image(url)

    if img is not None:
        img = optimize_image_width(img, max_image_width)
        save_image(img, dst_path)
        return {"url": url, "path": dst_prd_path}
    else:
        return {"url": url, "path": None}

def replace_image_urls(text, url, path):
    """ ![hoge](url) を置換する

    ![hoge](url)を <img href='path' origin_url='url' alt='hoge'/>に置換

    Args:
        text (string): 
        url (string): replaceされるURL
        path (string): replaceするURL
    """
    pattern = r'^\s*!\[(.+)\]\('+url+'\)$'
    texts = []
    for t in text.split('\n'):
        if re.match(pattern, t):
            alt = re.sub(pattern, r'\1', t)
            t = f"<img src='{path}' origin_url='{url}' alt='{alt}' />"
        texts += [t]
    return "\n".join(texts)

