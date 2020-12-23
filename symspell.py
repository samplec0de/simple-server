import numpy as np

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

freq_dict = {}
word2idx = {}
idx2word = []
transfeme = {}
vocab = []


def prepare_dict():
    to2 = open("dict_of_chast.txt", "r", encoding='utf-8').readlines()
    dict = {}
    ind = 0

    for i in to2:
        slovo = i.split("\t")
        if ind % 1000 == 0:
            print(ind)
        text = slovo[1]
        text = morph.parse(text)[0]
        if "u" in text.word:
            continue
        for j in text.lexeme:
            dict.update({j.word: float(slovo[10])})
        ind += 1

    dict = sorted(dict.items(), key=lambda x: -x[1])

    return dict

def precalc_symspell():
    def get_vocab():
        rus_text = []

        with open('dict_of_words.txt', 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            rus_text += lines

        vocab = sorted(set(rus_text))

        word2idx = {word: index for index, word in enumerate(vocab)}
        idx2word = np.array(vocab)

        transfeme = {}
        for word in idx2word:
            for i in range(len(word) - 2):
                if word[i:i + 3] not in transfeme:
                    transfeme[word[i:i + 3]] = 0
                transfeme[word[i:i + 3]] += 1

        return word2idx, idx2word, transfeme, vocab

    def gen_symspell(idx2word):
        symspell_dict = {}
        genered_from = {}
        for i in idx2word:
            genered_from[i] = i
            if i not in symspell_dict:
                symspell_dict[i] = 0
            symspell_dict[i] += 1
            for j in range(len(i)):
                new_str = i[:j] + i[j + 1:]
                if new_str not in symspell_dict:
                    symspell_dict[new_str] = 0
                symspell_dict[new_str] += 1
                genered_from[new_str] = i
        return symspell_dict, genered_from

    freq_dict = prepare_dict()
    word2idx, idx2word, transfeme, vocab = get_vocab()
    symspell_dict, genered_from = gen_symspell(idx2word)
    return freq_dict, word2idx, idx2word, transfeme, vocab, symspell_dict, genered_from

def init():
    global freq_dict, word2idx, idx2word, transfeme, vocab, symspell_dict, genered_from
    freq_dict, word2idx, idx2word, transfeme, vocab, symspell_dict, genered_from = precalc_symspell()

def count_probability(s1):
    cur = 0
    for i in range(len(s1) - 2):
        if s1[i:i + 3] not in transfeme:
            continue
        cur += transfeme[s1[i:i + 3]]
    cur = cur / (len(s1) - 2)
    if s1 in freq_dict:
        cur *= freq_dict[s1]
    return cur


def solve_with_symspell(start_string):
    lst_text = start_string.split()
    finish_string = ''
    for word in lst_text:
        if word in vocab or len(word) < 3:
            finish_string += (word + ' ')
            continue
        if len(word) == 3:
            possible = []
            for i in range(len(word)):
                if (word[:i] + word[i + 1:]) in symspell_dict.keys():
                    possible.append(word[:i] + word[i + 1:])
            if len(possible):
                word = possible[0]
            finish_string += (word + ' ')
            continue
        if word not in symspell_dict:
            possible = []
            for i in range(len(word)):
                # print(word[:i] + word[i + 1:])
                if (word[:i] + word[i + 1:]) in symspell_dict.keys():
                    possible.append(word[:i] + word[i + 1:])

            if len(possible):
                s = word
                good = 0
                for s1 in possible:
                    cur = count_probability(s1)
                    if (cur / len(s1)) > good:
                        good = cur
                        s = s1
                word = s
        if word in vocab:
            finish_string += (word + ' ')
            continue
        if word in genered_from.keys():
            finish_string += (genered_from[word] + ' ')
        else:
            finish_string += (word + ' ')
    return finish_string