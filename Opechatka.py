from heapq import *
import pymorphy2

to2 = open("dict_of_chast.txt", "r",  encoding='utf-8').readlines()

to = open("dict_of_words.txt", "r",  encoding='utf-8').readlines()

dict = {}
dict2 = {}
morph = pymorphy2.MorphAnalyzer()
ind = 0

for i in to:
    if ind % 1000 == 0:
        print(ind)
    text = i[:-1]
    text = morph.parse(text)[0]
    if "u" in text.word:
        continue
    for j in text.lexeme:
        dict.update({j.word: 1})
    ind += 1

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
        dict2.update({j.word: float(slovo[10])})
    ind += 1


dict2 = sorted(dict2.items(), key=lambda x: -x[1])
dict = sorted(dict.items(), key=lambda x: -x[1])

print(len(dict))


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


def add_bor2(s, ind_s, num, k):
    global ind2, h2
    if ind_s == len(s):
        h2[num].k = k
        h2[num].term = True
        return
    if s[ind_s] not in h2[num].verh.keys():
        h2[num].verh[s[ind_s]] = ind2 + 1
        h2.append(Bukva())
        ind2 += 1
        add_bor(s, ind_s + 1, ind2, k)
    else:
        add_bor(s, ind_s + 1, h2[num].verh[s[ind_s]], k)


root = 0
root2 = 0
ind = 0
h = [Bukva()]
ind2 = 0
h2 = [Bukva()]

# print(len(dict))
keyboard = ["ёйцукенгшщзхъ", "фывапролджэ", "ячсмитьбю"]
ver = [[0] * 34 for i in range(34)]
k1 = [0.999, 0.4, 0.1, 0.05, 0.001]
for i in range(3):
    for j in range(len(keyboard[i])):
        for i1 in range(3):
            for j1 in range(len(keyboard[i1])):
                ver[ord(keyboard[i][j]) - ord('а')][ord(keyboard[i1][j1]) - ord('а')] = k1[min(4, (abs(i1 - i) + abs(j1 - j)))]


ver[ord("а") - ord('а')][ord("о") - ord('а')] = 0.2
ver[ord("о") - ord('а')][ord("а") - ord('а')] = 0.2
ver[ord("е") - ord('а')][ord("ё") - ord('а')] = 0.999
ver[ord("ё") - ord('а')][ord("е") - ord('а')] = 0.999

summ = 0
for i in dict2:
    summ = max(i[1], summ)
for i in dict:
    s = ""
    if i[0] == "<UNK>" or i[0] == "<NUM>":
        continue
    for j in i[0]:
        if j.isalpha():
            s += j
    add_bor(s, 0, root, 1)

for i in dict2:
    s = ""
    if i[0] == "<UNK>" or i[0] == "<NUM>":
        continue
    for j in i[0]:
        if j.isalpha():
            s += j
    add_bor2(s, 0, root2, i[1] / summ)


used = set()
used2 = set()


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
            if h[e[1]].term:
                print(e[0], e[3])
                if e[0] * h[e[1]].k < ans:
                    ans = e[0] * h[e[1]].k
                    anss = e[3]
        if e[0] < ans and (e[1], e[2]) not in used:
            for i in h[e[1]].verh.items():
                # print(i, (e[0] * ver[i[0]][ord(s[e[2]]) - ord('а')]))
                if e[2] == len(s):
                    heappush(q, (0.15 * e[0], e[1], e[2], e[3], e[4] + 1))
                else:
                    if e[4] + (s[e[2]] != i[0]) <= c1:
                      # print(i[0], s[e[2]])
                      heappush(q,
                              (e[0] * ver[ord(i[0]) - ord('а')][ord(s[e[2]]) - ord('а')], i[1], e[2] + 1, e[3] + i[0], e[4] +
                                (s[e[2]] != i[0])))
                    if e[4] < c1:
                        heappush(q, (0.15 * e[0], e[1], e[2] + 1, e[3], e[4] + 1))
                        heappush(q, (e[0] * 0.2, i[1], e[2], e[3] + i[0], e[4] + 1))
            used.add((e[1], e[2]))
        if e[0] > ans:
            break
    # print("OK")
    return [anss, ans]


def get_ans2(s, k, c1):
    global used
    q = []
    ans = 0
    anss = ""
    heappush(q, (-1, 0, 0, '', 0, 0))
    # print(q)
    # print("ти лох")
    while len(q):
        e = heappop(q)
        print(e)
        if e[2] == len(s):
            if h2[e[1]].term:   
                if e[0] * h2[e[1]].k < ans:
                    print(e[0] * h2[e[1]].k)
                    ans = e[0] * h2[e[1]].k
                    anss = e[3]
        if e[0] < ans and (e[1], e[2]) not in used:
            for i in h2[e[1]].verh.items():
                # print(i, (e[0] * ver[i[0]][ord(s[e[2]]) - ord('а')]))
                if e[2] == len(s):
                    heappush(q, (0.15 * e[0], e[1], e[2], e[3], e[4] + 1))
                else:
                    if e[4] + (s[e[2]] != i[0]) <= c1:
                      heappush(q,
                              (e[0] * ver[ord(i[0]) - ord('а')][ord(s[e[2]]) - ord('а')], i[1], e[2] + 1, e[3] + i[0], e[4] +
                                (s[e[2]] != i[0])))
                    if e[4] < c1:
                        heappush(q, (0.15 * e[0], e[1], e[2] + 1, e[3], e[4] + 1))
                        heappush(q, (e[0] * 0.2, i[1], e[2], e[3] + i[0], e[4] + 1))
            used.add((e[1], e[2]))
        if e[0] > ans:
            break
    return [anss, ans]


def fix_text(t):
    global used
    ans1 = ""
    ans2 = ""
    s = ""
    for j in t.lower():
        if j.isalpha():
            s += j
        else:
            try:
                used = set()
                slovo = get_ans(s, 1, 3)
                used = set()
                slovo2 = get_ans2(s, 1, 3)
                print(slovo2, "!")
                if s != "" and slovo[0] != "" and slovo2[1] <= 0.05:
                    # print(s)
                    ans2 += slovo[0]
                    ans1 += s
                elif s != "" and slovo2[1] >= 0.05:
                    ans1 += s
                    ans2 += slovo2[0] + "!"
                else:
                    ans1 += s
                    ans2 += s
                ans2 += j
                ans1 += j
            except:
                ans1 += s
                ans1 += j
                ans2 += s
                ans2 += j
            s = ""
    print(ans1, ans2)
    try:
        used = set()
        print(s)
        # print(s)
        slovo = get_ans(s, 1, 3)
        used = set()
        slovo2 = get_ans2(s, 1, 3)
        print(slovo, "    and   ", slovo2, "!")
        if s != "" and slovo[0] != "" and slovo2[1] <= 0.05:
            # print(s)
            ans2 += slovo[0]
            ans1 += s
        elif s != "" and slovo2[1] >= 0.05:
            ans1 += s
            ans2 += slovo2[0] + "!"
        else:
            ans1 += s
            ans2 += s
    except:
        print('лох')
        ans1 += s
        ans2 += s
    print(ans1, ans2)
    return ans2