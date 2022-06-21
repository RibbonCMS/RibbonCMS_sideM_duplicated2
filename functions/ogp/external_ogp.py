""" 外部OGPの取得

Output:
    `front/contents/etc/external_ogp.json`
"""

import os
import json
from urllib.parse import urlparse

from py_ogp_parser.parser import request

def dl_ogp(url):
    try:
        status_code, result = request(url)
        url_parsed = urlparse(url)
        metadata = {
            'url_domain': url_parsed.netloc,
            'url_domain_link': f"{url_parsed.scheme}://{url_parsed.netloc}",
            'title': None,
            'description': None,
            'image_url': None,
            'site_name': None,
        }
        if 'title' in result.keys():
            metadata['title'] = result['title']
        if 'ogp' in result.keys():
            ogp = result['ogp']
            if 'og:description' in ogp.keys():
                metadata['description'] = ogp['og:description'][0]
            if 'og:image' in ogp.keys():
                metadata['image_url'] = ogp['og:image'][0]
            if 'og:site_name' in ogp.keys():
                metadata['site_name'] = ogp['og:site_name'][0]
        return metadata
    except:
        return None

def save_ogp(ogp_dict, save_path):
    save_dir = "/".join(save_path.split('/')[:-1])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(save_path, 'w', encoding="utf-8") as f:
        json.dump(ogp_dict, f, indent=4, ensure_ascii=False)

def load_ogp(load_path):
    if not os.path.exists(load_path):
        return {}
    with open(load_path, "r") as f:
        return json.load(f)

