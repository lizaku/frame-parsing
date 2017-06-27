from create_features import features
from sklearn.externals import joblib
from pymystem3 import Mystem
from collections import OrderedDict
from string import whitespace, punctuation

clf = joblib.load('frame_parser.pkl')
vec = joblib.load('feature_transformer.pkl')
m = Mystem()

def frames(sentence):
    header = ('word', 'lex', 'pos', 'gram', 'prev_gr', 'prev_lex', 'rel', 'pred_lemma')
    anas = m.analyze(sentence)
    fr = OrderedDict()
    data = OrderedDict()
    for w in anas:
        word = w['text']
        #if word in whitespace or word in punctuation:
        #    continue
        try:
            gr = w['analysis'][0]['gr']
            lex = w['analysis'][0]['lex']
        except:
            gr, lex = None, None
        data[word] = [lex, gr, None, None, None, None]
    vector = features(data)
    vectors = OrderedDict((k, v) for k,v in vector.items() if k not in whitespace and k not in punctuation)
    for w in vectors:
        feats = [w] + [str(x) for x in vectors[w]][:-1]
        feats = dict(zip(header, feats))
        v = vec.transform(feats)
        role = clf.predict(v)[0]
        fr[w] = role
    #print(fr)
    return fr
    #vector = vec.transform(features)
    #return clf.predict(vector)[0][0]

if __name__ == "__main__":
    # clf = joblib.load('model.pkl')
    # vec = joblib.load('feature_transformer.pkl')

    # demo part
    phrase = input('Введите фразу: ')
    fr = frames(phrase)
    #print(fr)
    for f in fr:
        print(f, fr[f])
    #words = phrase.split()
    #for word in words:
    #    print(word, pos(word))
