""" issueがcloseされたときに実行されるプログラム

issueのラベルを見て適切な関数を実行する。
{Issue label} -> function():
    delete -> src.delete.delete_article()
    article -> src.article.build_article()
    fixed/* -> src.fixed.build_fixed()
    config -> src.config.build_config()
"""

import argparse

from src.article import build_article
from src.config import build_config
from src.delete import delete_article
from src.fixed import build_fixed
from models.issue import Issue
from models.consts import Consts
from functions.utils import color


def main(consts):
    print(f"{color('Consts Params:', 'LIGHT_RED')}")

    print(consts)

    issue = Issue(consts.ISSUE_PATH)
    print(f"\n{color('Issue Params:', 'LIGHT_RED')}")
    print(issue)

    if issue.is_include([consts.ARTICLE_FLAG_LABEL]):
        build_article(consts, issue)
    elif issue.is_include([consts.CONFIG_FLAG_LABEL]):
        build_config(consts, issue)
    elif issue.is_include([consts.DELETE_FLAG_LABEL]):
        delete_article(consts, issue)
    elif issue.is_include([consts.FIXED_FLAG_LABEL]):
        build_fixed(consts, issue)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test_dir', type=str, default='')
    args = parser.parse_args()

    test_dir = args.test_dir if args.test_dir != '' else None
    consts = Consts(test_dir=test_dir)

    main(consts)

