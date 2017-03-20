import csv
import os
import json
from collections import OrderedDict


def predicates(in_f):
    preds = {}
    with open(in_f, 'r', encoding='utf-8') as f:
        js = f.read()
    examples = json.loads(js, object_pairs_hook=OrderedDict)
    for ex in examples:
        len_words = len(examples[ex])
        n_word = 0
        for w in examples[ex]:
            if n_word == 0:
                prev_word = None
            instance = examples[ex][w]
            try:
                lex, gr, sem, sem2, role, rank = instance
            except:
                instance = instance[:7] + instance[8:]
            try:
                pos, gram = gr.split(' ', maxsplit=1)
            except ValueError:
                try:
                    pos, gram = gr.split(',', maxsplit=1)
                except:
                    pos, gram = gr, None
            prev_gr, prev_lex = None, None
            if prev_word:
                prev_lex, prev_gr = prev_word[0:2]
            if instance[-1] is None and instance[-2] is None:
                n_word += 1
                preds[(ex, w)] = [lex, pos, gram, sem, sem2, n_word, prev_gr, prev_lex, 0]
                prev_word = instance
                continue
            if instance[-1] == 'Предикат':
                preds[(ex, w)] = [lex, pos, gram, sem, sem2, n_word, prev_gr, prev_lex, 1]
                prev_word = instance
            n_word += 1
    with open('predicates.csv', 'w', encoding='utf-8') as p:
        header = ('ExID', 'Wordform', 'Lex', 'POS', 'Gram', 'Sem', 'Sem2', 'WordID', 'prev_lex', 'prev_gr', 'Predicate')
        p.write('\t'.join(header) + '\n')
        for pr in preds:
            p.write('\t'.join(list(pr) + [str(x) for x in preds[pr]]) + '\n')
            
def arguments(in_f):
    args = {}
    with open(in_f, 'r', encoding='utf-8') as f:
        js = f.read()
    examples = json.loads(js, object_pairs_hook=OrderedDict)
    for ex in examples:
        len_words = len(examples[ex])
        n_word = 0
        for w in examples[ex]:
            if n_word == 0:
                prev_word = None
            instance = examples[ex][w]
            try:
                lex, gr, sem, sem2, role, rank = instance
            except:
                instance = instance[:7] + instance[8:]
            try:
                pos, gram = gr.split(' ', maxsplit=1)
            except ValueError:
                try:
                    pos, gram = gr.split(',', maxsplit=1)
                except:
                    pos, gram = gr, None
            prev_gr, prev_lex = None, None
            if prev_word:
                prev_lex, prev_gr = prev_word[0:2]
            if instance[-1] is None and instance[-2] is None:
                n_word += 1
                args[(ex, w)] = [lex, pos, gram, sem, sem2, n_word, prev_gr, prev_lex, 'noclass']
                prev_word = instance
                continue
            if instance[-1] != 'Предикат' and instance[-2] != '-':
                print(role)
                args[(ex, w)] = [lex, pos, gram, sem, sem2, n_word, prev_gr, prev_lex, role]
                prev_word = instance
            n_word += 1
    with open('arguments.csv', 'w', encoding='utf-8') as p:
        header = ('ExID', 'Wordform', 'Lex', 'POS', 'Gram', 'Sem', 'Sem2', 'WordID', 'prev_lex', 'prev_gr', 'Class')
        p.write('\t'.join(header) + '\n')
        for a in args:
            p.write('\t'.join(list(a) + [str(x) for x in args[a]]) + '\n')
    

if __name__ == '__main__':
    #predicates('parsed_framebank_roles_small.json')
    arguments('parsed_framebank_roles_small.json')
