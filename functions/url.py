""" URLに関する処理

URLのパースなどを行う
"""
import re

def parse_raw_url(text):
    pattern = r'^\s*https?:\/\/\S+[^\S\n\r]*$'
    urls = []
    for t in text.split('\n'):
        is_match = re.match(pattern, t)
        if is_match:
            urls += [t]
    return urls

def parse_image_url(text):
    pattern = r'^\s*!\[.+\]\((https?:\/\/\S+)\)$'
    images = []
    for t in text.split('\n'):
        if re.match(pattern, t):
            images += [re.sub(pattern, r'\1', t)]
    return images

