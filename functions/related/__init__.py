""" 関連記事の計算プログラム

- `functions/tokenizer/**.py`
- `functions/vectorizer/**.py`
などを使って記事をベクトル化し，全ての関連記事を計算する．

Output:
    `front/contents/etc/related_articles.json`
"""

import os
import re
import json

import numpy as np

from functions.utils import import_module_with_install, color


def related(
            articles, 
            related_dir,
            model,
            k=4,
        ):
    clean_patterns = _compile_clean_patterns()
    texts = [_make_text(article, clean_patterns) for article in articles]
    slugs = np.array([article.slug for article in articles])
    model = _get_model(model)

    vectors = model.vectorize(texts)
    scores = _score(vectors)
    slugs = _sort_slugs_by_score(scores, slugs, k)
    _save(slugs, related_dir)

def _get_model(model):
    try:
        model = import_module_with_install(f'functions.related.models.{model}')
        print(
            color(' model', 'CYAN') + ' =',
            color(f'{config["related_model"]}', "BROWN"),
        )
    except:
        model = import_module_with_install(f'functions.related.models.default')
        print(
            color(' model', 'CYAN') + ' =',
            color(f'default', "BROWN"),
        )
    return model

def _make_text(article, clean_patterns):
    title = article.title
    markdown = article.markdown
    description = article.description
    text = f'{title} {markdown}'
    text = _cleaning_text(text, clean_patterns)
    return text

def _cleaning_text(text, clean_patterns):
    for pattern in clean_patterns:
        text = pattern.sub('', text)
    return text

def _compile_clean_patterns():
    clean_patterns = []
    clean_patterns += [re.compile(r"!\[.*\]\(https?://[a-zA-Z\d!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+\)")]
    clean_patterns += [re.compile(r"\[.*\]\(https?://[a-zA-Z\d!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+\)")]
    clean_patterns += [re.compile(r"https?://[a-zA-Z\d!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+")]
    return clean_patterns

def _score(vectors):
    X = vectors.dot(vectors.T)
    X[range(X.shape[0]), range(X.shape[1])] = np.inf
    return X

def _sort_slugs_by_score(scores, slugs, k):
    sorted_index = np.argsort(scores, axis=0)[::-1].T
    slugs_dict = {}
    for i, index in enumerate(sorted_index):
        slug = slugs[i]
        _slugs = slugs[index][1:k+1]
        slugs_dict[slug] = list(_slugs)
    return slugs_dict

def _save(slugs, related_dir):
    if not os.path.exists(related_dir):
        os.makedirs(related_dir)
    with open(f'{related_dir}/related_articles.json', 'w', encoding="utf-8") as f:
        json.dump(slugs, f, indent=4, ensure_ascii=False)

