""" 固定ページ更新関数

`fixed/{name}`のissueラベルで実行される．
`{name}`という名前の固定ページ用のjsonを生成する．

Output:
    `front/contents/fixed/{fixed_name}.json`
    `front/public/static/images/fixed/{fixed_name}/[md5].webp`
    (optional) `front/public/static/images/fixed/{fixed_name}/thumbnail.jpg`
"""

import os
import json

from models.fixed import Fixed
from functions.utils import color

def build_fixed(consts, issue):
    """ --- fixed pageの名前を取得 ---"""
    fixed_name = ''
    for label in issue.labels:
        name = label['name'].split('/')
        if name[0] == 'fixed':
            fixed_name = '/'.join(name[1:])
    assert fixed_name != '', "Issue needs `fixed/**` label."

    """ --- fixedの内容を取得 ---"""
    assert issue.fm is not None, "Issue needs frontmatter."
    fixed = issue.fm

    """ --- 画像を保存 --- """
    fixed = Fixed(fixed, fixed_name, consts)    
    print()
    print(color('Updated Fixed:', 'LIGHT_RED'))
    print(fixed)

    """ --- fixed/**.jsonを保存 --- """
    fixed.save()

