""" Sudachiで文章の形態素解析を行う．

形態素解析器を切り替えれるように入出力を考える

ToDo:
    ストップワードをこの関数で設定するか，`functions/vectorizer.py`で設定するかを決める．
    形態素解析器を切り替えることを考えるとこの関数内で実行出来た方が良さそう．
"""

import MeCab

def tokenize(text):
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(text)
    texts = []
    while node:
        part_of_speech = node.feature.split(',')
        if not _is_stopword(part_of_speech):
            texts += [node.surface]
        node = node.next
    return texts

def wakachi(text):
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(text)
    texts = []
    while node:
        texts += [node.surface]
        node = node.next
    return texts

def _is_stopword(part_of_speech):
    stopwords = ['BOS/EOS', '助詞', '助動詞', '記号']
    for stopword in stopwords:
        if stopword in part_of_speech:
            return True
    return False


""" sudachi tokenizer (duplicated) """
#from sudachipy import tokenizer
#from sudachipy import dictionary
#
#def tokenize(text):
#    mode = tokenizer.Tokenizer.SplitMode.B
#    _tokenizer = dictionary.Dictionary().create()
#    text = [m.normalized_form() for m in _tokenizer.tokenize(text, mode) if not _is_stopword(m.part_of_speech())]
#    return text
#
#def _is_stopword(part_of_speech):
#    stopwords_main =  ['助詞', '助動詞', '記号', '補助記号']
#    stopwords_sub = ['非自立可能']
#    is_stop = part_of_speech[0] in stopwords_main
#    is_stop = is_stop or part_of_speech[1] in stopwords_sub
#    return is_stop

