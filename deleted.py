""" issueがdeleteされたときに実行されるプログラム

issue idと一致するarticleなどを削除する
削除対象: 
    article
    thumbnail
    article images
    tags (記事を削除してなくなるタグの場合)
    related article
"""

import argparse

from src.delete import delete_article
from models.issue import Issue
from models.consts import Consts
from functions.utils import color

def main(consts):
    print(f"{color('Consts Params:', 'LIGHT_RED')}")

    print(consts)

    issue = Issue(consts.ISSUE_PATH)
    print(f"\n{color('Issue Params:', 'LIGHT_RED')}")
    print(issue)

    delete_article(consts, issue)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test_dir', type=str, default='')
    args = parser.parse_args()

    test_dir = args.test_dir if args.test_dir != '' else None
    consts = Consts(test_dir=test_dir)

    main(consts)


