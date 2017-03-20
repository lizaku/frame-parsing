import csv
import os
from lxml import etree
import json
from collections import OrderedDict


PATH = './isa_parser/data/original_framebank'

def extract_morpho(example):
    tree = etree.XML(example)
    res = OrderedDict()
    for se in tree:
        for w in se:
            if len(w) > 0:
                lex = w[0].attrib['lex']
                gr = w[0].attrib['gr']
                word = w[-1].tail
                sem = w[0].get('sem')
                sem2 = w[0].get('sem2')
                res[word] = [lex, gr, sem, sem2, None, None] # если в предложении есть одинаковые слова, они потеряются
            else:
                res[w.text] = [None*6]
    return res


def examples_write_csv(fname, examples):
    with open(fname, 'w', encoding='utf-8') as wr:
        out = csv.writer(wr, delimiter='\t')
        header = ('ExID', 'Wordform', 'Lex', 'Gr', 'Sem', 'Sem2', 'Role', 'Rank')
        out.writerow(header)
        for ex in examples:
            for w in examples[ex]:
                row = [ex] + [w] + examples[ex][w]
                out.writerow(row)


def examples_write_json(fname, examples):
    with open(fname.split('.')[0] + '.json', 'w',  encoding='utf-8') as wj:
        j = json.dumps(examples, ensure_ascii=False)
        wj.write(j)


def parse_framebank_examples(in_f, out_f):
    examples = OrderedDict()
    with open(os.path.join(PATH, in_f), 'r', encoding='utf-8') as ex:
        reader = csv.reader(ex, delimiter="\t")
        header = next(reader)
        i = 0
        for line in reader:
            #if i == 5000:
            #    break
            try:
                i += 1
                print(i)
                if not '<p' in line[1]:
                    line[1] = '<p>' + line[1] + '</p>'
                line[1] = line[1].split('</p>')[0] + '</p>'
                res = extract_morpho(line[1])
                examples[line[0]] = res # dictionary:
                # {ex_id: {word1: [lex, gr, sem, sem2]}, word2: [lex, gr, sem, sem2]}}
            except:
                pass # todo: parse all examples
    examples_write_csv(out_f, examples)
    examples_write_json(out_f, examples)
                
def parse_framebank_roles(parsed, in_f, out_f):
    examples = json.loads(open(parsed, 'r', encoding='utf-8').read(), object_pairs_hook=OrderedDict)
    with open(os.path.join(PATH, in_f), 'r', encoding='utf-8') as anno:
        reader = csv.reader(anno, delimiter="\t")
        header = next(reader)
        i = 0
        for line in reader:
            print(i)
            i += 1
            #print(line)
            constr_id, ex_id, place, phrase, word, form, role, rank, sem, \
            _, constrex_id, itemex_id, key_lexemes = line
            if '[' in word: # костыль
                continue
            elif len(word.split()) > 1 and ex_id in examples:
                print(ex_id, word)
                try:
                    examples[ex_id][word.split()[1]].append(role)
                    examples[ex_id][word.split()[1]].append(rank)
                    continue
                except:
                    continue
            elif len(word.split('-')) > 1 and ex_id in examples:
                print(ex_id, word)
                try:
                    examples[ex_id][word.split('-')[0]].append(role)
                    examples[ex_id][word.split('-')[0]].append(rank)
                    continue
                except:
                    continue
            elif word:
                try:
                    if ex_id in examples:
                        examples[ex_id][word][-1] = rank
                        examples[ex_id][word][-2] = role
                except KeyError:
                    continue # todo: parse all instances
    examples_write_json(out_f, examples)
    examples_write_csv(out_f, examples)



if __name__ == '__main__':
    #parse_framebank_examples('exampleindex.csv', 'parsed_framebank.csv')    
    parse_framebank_roles('parsed_framebank.json', 'framebank_anno_ex_items_fixed.txt', 'parsed_framebank_roles.csv')
