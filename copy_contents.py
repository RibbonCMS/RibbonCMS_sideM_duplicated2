""" コンテンツをフロントエンドにコピーする
"""

import argparse
import os
from glob import glob
import shutil

from models.consts import Consts
from functions.utils import color


def main(consts):
    print(f"{color('Consts Params:', 'LIGHT_RED')}")
    print(consts)
    print()

    origin = consts.NEXTJS_BASE_PATH
    dest = consts.NEXTJS_FRONTEND_BASE_PATH

    copy_all(origin, dest)

def copy_all(origin, dest):
    item_pathes = glob(f'{origin}/**/*.*', recursive=True)
    for item in item_pathes:
        origin_item = item
        dest_item = item.replace(origin, dest)
        dest_item_dir = '/'.join(dest_item.split('/')[:-1])
        if not os.path.exists(dest_item_dir):
            os.makedirs(dest_item_dir)
        shutil.copyfile(origin_item, dest_item)
        print(f'copied {color(origin_item, "BROWN")} -> {color(dest_item, "BROWN")}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test_dir', type=str, default='')
    args = parser.parse_args()

    test_dir = args.test_dir if args.test_dir != '' else None
    consts = Consts(test_dir=test_dir)

    main(consts)

