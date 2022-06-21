""" 記事削除関数

Delete:
    `front/contents/article/[slug]/index.md`
    [slug] item from `front/contents/etc/tags.json`
    [slug] item from `front/contents/etc/related_articles.json`
    [slug] item from `front/contents/etc/external_ogp.json`
    `front/public/static/images/thumbnail/[slug].jpg`
    `front/public/static/images/articles/[slug]/[md5].webp`
    `fromt/public/static/images/etc`
"""
import os
import shutil
from glob import glob

from models.article import Article
from functions.tags import load_tags, save_tags
from functions.related import related
from functions.utils import color

def delete_article(consts, issue):
    slug = issue.id
    print()
    print(color('Delete Article: ', "LIGHT_RED"), color(slug, "BROWN"))

    """
    ------------------
    --- 記事の削除 ---
    ------------------
    """
    article_path = f'{consts.MD_DIR}/{slug}/'
    if os.path.exists(article_path):
        print('delete', article_path)
        shutil.rmtree(article_path)

    """
    ------------------------
    --- サムネイルの削除 ---
    ------------------------
    """
    thumbnail_path = f'{consts.THUMBNAIL_IMAGES_DIR}/{slug}.{consts.THUMBNAIL_EXTENSION}'
    if os.path.exists(thumbnail_path):
        print('delete', thumbnail_path)
        os.remove(thumbnail_path)

    """
    ----------------------
    --- 記事画像の削除 ---
    ----------------------
    """
    images_path = f'{consts.ARTICLE_IMAGES_DIR}/{slug}/'
    if os.path.exists(images_path):
        print('delete', images_path)
        shutil.rmtree(images_path)

    """
    ------------------
    --- Tagsの更新 ---
    ------------------
    """
    """ --- 全記事の取得 ---"""
    slugs = [p.split('/')[-1] for p in glob(f'{consts.MD_DIR}/*')]
    articles = [Article.from_article(consts.MD_DIR, slug) for slug in slugs]

    """ --- Tagsの更新処理 --- """
    tags_dir = f'{consts.ETC_DIR}'
    tags = load_tags(tags_dir)

    updated_tags = {}
    for article in articles:
        for tag_id in article.tag_ids:
            updated_tags[tag_id] = tags[str(tag_id)]

    save_tags(updated_tags, tags_dir)
    print('update', f'{tags_dir}/tags.json')

    """ --- 関連記事の算出 --- """
    print()
    print(color('Create Related:', "LIGHT_RED"))
    related(
            articles,
            related_dir=consts.ETC_DIR,
            model=config["related_model"],
            k=10,
        )

