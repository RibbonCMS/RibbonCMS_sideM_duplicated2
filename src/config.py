""" Config更新関数

`config`のissueラベルで実行される．
サイト名やAuthor名，basePathなどを登録する．

Output:
    `front/contents/etc/config.json`
    `front/public/static/images/avatar.webp`
    `front/public/static/favicon.ico`
    `front/next.config.ts`
"""

from models.config import Config
from functions.utils import color

def build_config(consts, issue):
    config = Config.from_issue(issue, consts)

    print()
    print(f"{color('Create Config:', 'LIGHT_RED')}")

    config.save()
    print(config)

