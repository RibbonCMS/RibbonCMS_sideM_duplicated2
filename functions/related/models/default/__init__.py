""" tf-idfで文章をベクトルに変換する

Inputs:
    string[][]: 分かち書きした文章群

Returns:
    ndarray
"""

from sklearn.feature_extraction.text import TfidfVectorizer

from functions.related.models.default import tokenizer

def vectorize(texts):
    vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize)
    X = vectorizer.fit_transform(texts)
    X = X.toarray()
    return X

def tokenize(text):
    return tokenizer.wakachi(text)

