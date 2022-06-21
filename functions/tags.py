""" etc/tags.jsonを更新したりする処理

Attributes:
    tags (Dict): Tags dictionary
        Dict:
            "tag_id": string
                "name": string
                "color": string
                "description": string,
"""

import os
import json

def load_tags(tags_dir):
    tags_file = f"{tags_dir}/tags.json"
    if not os.path.exists(tags_file):
        return {}
    with open(tags_file, "r") as f:
        tags = json.load(f)
    return tags


def save_tags(tags, tags_dir):
    if not os.path.exists(tags_dir):
        os.makedirs(tags_dir)
    with open(f"{tags_dir}/tags.json", 'w', encoding="utf-8") as f:
        json.dump(tags, f, indent=4, ensure_ascii=False)


