""" 記事更新関数

Output:
    `front/contents/article/[slug]/index.md`
    `front/contents/etc/tags.json`
    `front/contents/etc/related_articles.json`
    `front/contents/etc/external_ogp.json`
    `front/public/static/images/thumbnail/[slug].jpg`
    `front/public/static/images/articles/[slug]/[md5].webp`
"""

from glob import glob
import json

from models.article import Article
from models.config import Config
from functions.utils import color, is_future_than
from functions.ogp.generate_ogp_image import generate_ogp_image
from functions.ogp.external_ogp import dl_ogp, save_ogp, load_ogp
from functions.url import parse_raw_url, parse_image_url
from functions.images import dl_save_image, replace_image_urls
from functions.tags import load_tags, save_tags
from functions.related import related

def build_article(consts, issue):
    """
    ------------------
    --- 記事の更新 ---
    ------------------
    """
    article = Article.from_article(consts.MD_DIR, issue.id)

    print(f'\nLoad article from {consts.MD_DIR}/{issue.id}/')
    print(f"{color('Loaded Article Params:', 'LIGHT_RED')}")
    print(article)

    tag_ids = [label['id'] for label in issue.labels if 
                len(label['name'].split('/'))>=2 and
                label['name'].split('/')[0]=='tag'
                ]

    description = issue.get_fm('ogp_description')
    if description is None or description == '':
        description = issue.md.replace('\n', ' ')[:200]
        if len(issue.md) > 200:
            description += '...'

    """ issue frontmatterで投稿日時が指定されている場合それを使う """
    issue.posted_at = issue.get_fm('posted_at')
    if issue.posted_at is None:
        issue.posted_at = issue.closed_at

    print()
    if article.posted_at is None:
        """ 新規投稿 """
        posted_at = issue.posted_at
        updated_at = ''
        print('新規投稿')
    elif is_future_than(issue.posted_at, issue.closed_at):
        """ 投稿済み投稿の公開時間の変更(指定時間が未来なので無条件で未公開化) """
        posted_at = issue.posted_at
        updated_at = ''
        print('投稿済み投稿の公開時間の変更')
    elif is_future_than(article.posted_at, issue.closed_at):
        """ 投稿済み未公開投稿の公開時間の変更(指定時間が過去・現在未公開なので公開される) """
        posted_at = issue.posted_at
        updated_at = ''
        print('投稿済み未公開投稿の公開時間の変更')
    else:
        """ 投稿・公開済み投稿の更新時間の変更(指定時間が過去・公開済みなので現在時間に更新した扱いになる) """
        posted_at = None
        updated_at = issue.closed_at
        print('投稿・公開済み投稿の更新時間の変更')

    article.update(
            slug=issue.id,
            title=issue.title,
            markdown=issue.md,
            posted_at = posted_at,
            updated_at = updated_at,
            tag_ids=tag_ids,
            description=description,
        )

    """ グローバルコンフィグのロード """
    config = Config.load(consts)

    """
    ------------------------
    --- サムネ画像の生成 ---
    ------------------------
    """
    thumbnail_save_path = f'{consts.THUMBNAIL_IMAGES_DIR}/{article.slug}.{consts.THUMBNAIL_EXTENSION}'
    generate_ogp_image(issue, article, config, consts, thumbnail_save_path)

    """
    --------------------------
    --- 画像のダウンロード ---
    --------------------------
    """
    image_urls = parse_image_url(article.markdown)
    for url in image_urls:
        image_url = dl_save_image(
            url=url,
            save_dir=f'{consts.ARTICLE_IMAGES_DIR}/{article.slug}',
            save_dir_prd=f'{consts.ARTICLE_IMAGES_DIR_PRD}/{article.slug}',
            extension='webp',
            max_image_width=600,
        )
        if image_url['path'] is not None:
            article.markdown = replace_image_urls(
                    text=article.markdown,
                    url=url,
                    path=image_url['path'],
                )

    article.save(consts.MD_DIR)
    print(f"{color('Updated Article Params:', 'LIGHT_RED')}")
    print(article)

    """
    -------------------------
    --- OGPのダウンロード ---
    -------------------------
    """
    external_urls = parse_raw_url(article.markdown)
    external_ogp_json_path = f'{consts.ETC_DIR}/external_ogp.json'
    ogp_dict = load_ogp(external_ogp_json_path)
    for url in external_urls:
        ogp = dl_ogp(url)
        if ogp is not None:
            if ogp['image_url'] is not None:
                image_url = dl_save_image(
                    url=ogp['image_url'],
                    save_dir=f'{consts.EXTERNAL_IMAGES_DIR}/',
                    save_dir_prd=f'{consts.EXTERNAL_IMAGES_DIR_PRD}/',
                    extension='webp',
                    max_image_width=600,
                )
                if image_url['path'] is not None:
                    """ DLした画像のパスを使う """
                    ogp['image_url'] = image_url['path']
            ogp_dict[url] = ogp
    save_ogp(ogp_dict, external_ogp_json_path)
    
    
    """
    ----------------------
    --- タグ一覧の更新 ---
    ----------------------
    """

    """ --- 全記事の取得 --- """
    slugs = [p.split('/')[-1] for p in glob(f'{consts.MD_DIR}/*')]
    articles = [Article.from_article(consts.MD_DIR, slug) for slug in slugs]

    """ issueのラベルをタグに追加 """
    tags_dir = f'{consts.ETC_DIR}'
    tags = load_tags(tags_dir)

    labels = issue.labels if issue.labels is not None else []
    for label in labels:
        sp_label_name = label['name'].split('/')
        if len(sp_label_name)>=2 and sp_label_name[0]=='tag':
            name = '/'.join(sp_label_name[1:])
            tag_id = str(label["id"])
            tag_color = label["color"]
            description = label["description"]
            tags[tag_id] = {
                'name': name,
                'color': tag_color,
                'description': description,
            }

    """ --- 使ってないタグを削除 --- """
    updated_tags = {}
    for article in articles:
        for tag_id in article.tag_ids:
            updated_tags[tag_id] = tags[str(tag_id)]

    save_tags(updated_tags, tags_dir)

    print()
    print(
        color('Updated Tags:\n', "LIGHT_RED"), 
        color('tags', 'CYAN') + ' =', 
        color(updated_tags, "BROWN"),
    )

    """
    ----------------------
    --- 関連記事の更新 ---
    ----------------------
    """
    print()
    print(color('Create Related:', "LIGHT_RED"))
    related(
            articles,
            related_dir=consts.ETC_DIR,
            model=config["related_model"],
            k=10,
        )

