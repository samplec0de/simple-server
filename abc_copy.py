'''from heapq import *
import re
import string
import pymorphy2
from collections import Counter

import requests
import tqdm
from bs4 import BeautifulSoup

url = "http://dict.ruslang.ru/freq.php?act=show&dic=freq_freq&title=%D7%E0%F1%F2%EE%F2%ED%FB%E9%20%F1%EF%E8%F1%EE%EA%20%EB%E5%EC%EC"

to = open("dict_of_words", "w")

def remove_spec_part_from_token(token):
    for spec_token in ['<NUM>', '<UNK>']:
        if spec_token in token and token != spec_token:
            token = re.sub(spec_token, '', token)
    return token


def prepare_page(url):
    print("!")
    page = requests.get(url)
    print("!")
    if page.status_code != 200:
        raise RuntimeError('Не смогли получить страницу')
    print("!")
    page = BeautifulSoup(page.text, 'html.parser')
    return page


def process_text(text):
    text = text.lower()
    text = re.sub('[{}]'.format(string.punctuation), ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub('[a-zA-Z]+[0-9]*', '<UNK>', text)
    text = ' '.join(map(remove_spec_part_from_token, text.split()))
    return text


page = prepare_page(url)
words = page.findAll('td')
dict = {}
morph = pymorphy2.MorphAnalyzer()
for i in range(15, len(words), 12):
    text = process_text(words[i].text)
    text2 = process_text(words[i + 7].text)
    ch = int(text2.split()[0])
    text = morph.parse(text)[0]
    if "u" in text.word:
        continue
    for i in text.lexeme:
        dict.update({i.word: ch})

dict = sorted(dict.items(), key=lambda x: -x[1])


class Bukva():
    def __init__(self):
        self.verh = {}
        self.term = False
        self.k = 0

def add_bor(s, ind_s, num, k):
    global ind, h
    if ind_s == len(s):
        h[num].k = k
        h[num].term = True
        return
    if s[ind_s] not in h[num].verh.keys():
        h[num].verh[s[ind_s]] = ind + 1
        h.append(Bukva())
        ind += 1
        add_bor(s, ind_s + 1, ind, k)
    else:
        add_bor(s, ind_s + 1, h[num].verh[s[ind_s]], k)

root = 0
ind = 0
h = [Bukva()]

# print(len(dict))
keyboard = ["ёйцукенгшщзхъ", "фывапролджэ", "ячсмитьбю"]
ver = [[0] * 34 for i in range(34)]
k1 = 0.6
for i in range(3):
    for j in range(len(keyboard[i])):
        for i1 in range(3):
            for j1 in range(len(keyboard[i1])):
                ver[ord(keyboard[i][j]) - ord('а')][ord(keyboard[i1][j1]) - ord('а')] = 0.999 / \
                                                                                        ((abs(i1 - i) + abs(
                                                                                            j1 - j)) + 1)

ver[ord("а") - ord('а')][ord("о") - ord('а')] = 0.1
ver[ord("о") - ord('а')][ord("а") - ord('а')] = 0.1

summ = 0
for i in dict:
    summ += i[1]
for i in dict:
    s = ""
    if i[0] == "<UNK>" or i[0] == "<NUM>":
        continue
    for j in i[0]:
        if j.isalpha():
            s += j
    add_bor(s, 0, root, i[1] / summ)


used = set()


def get_ans(s, k, c1):
    global used
    q = []
    ans = 0
    anss = ""
    heappush(q, (-1, 0, 0, '', 0, 0))
    # print(q)
    # print("ти лох")
    while len(q):
        e = heappop(q)
        # print(e)
        if e[2] == len(s):
            # print(e[0], e[3])
            if h[e[1]].term:
                # print(e[0], e[3])
                if e[0] * h[e[1]].k < ans:
                    ans = e[0] * h[e[1]].k
                    anss = e[3]
        elif e[0] < ans and (e[1], e[2]) not in used:
            for i in h[e[1]].verh.items():
                # print(i, (e[0] * ver[i[0]][ord(s[e[2]]) - ord('а')]))
                if e[4] + (s[e[2]] != i[0]) <= c1:
                  # print(i[0], s[e[2]])
                  heappush(q,
                          (e[0] * ver[ord(i[0]) - ord('а')][ord(s[e[2]]) - ord('а')], i[1], e[2] + 1, e[3] + i[0], e[4] +
                            (s[e[2]] != i[0])))
                if e[4] < c1:
                    heappush(q, (0.15 * e[0], e[1], e[2] + 1, e[3], e[4] + 1))
                    heappush(q, (e[0] * 0.2, i[1], e[2], e[3] + i[0], e[4] + 1))
            used.add((e[1], e[2]))
    # print("OK")
    return [anss, ans]


def generate_text(t):
    global used
    ans = ""
    for i in t.split():
        s = ''
        for j in i:
            if j.isalpha():
                s += j
            else:
                try:
                    used = set()
                    if s != "":
                        # print(s)
                        ans += f'{s} ({get_ans(s, 1, 5)[0]}) '
                    ans += j
                except:
                    ans += s
                    ans += j
                s = ""
        try:
            used = set()
            # print(s)
            if s != "":
                ans += f'{s} ({get_ans(s, 1, 5)[0]}) '
        except:
            ans += s
    print(ans)
    return ans
'''