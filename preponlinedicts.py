import re
import string


import requests

from bs4 import BeautifulSoup

url_freq_dict = "http://dict.ruslang.ru/freq.php?act=show&dic=freq_freq&title=%D7%E0%F1%F2%EE%F2%ED%FB%E9%20%F1%EF%E8%F1%EE%EA%20%EB%E5%EC%EC"

def make_dict():
    def remove_spec_part_from_token(token):
        for spec_token in ['<NUM>', '<UNK>']:
            if spec_token in token and token != spec_token:
                token = re.sub(spec_token, '', token)
        return token

    def prepare_page(url):
        page = requests.get(url)
        if page.status_code != 200:
            raise RuntimeError('Не смогли получить страницу')
        page = BeautifulSoup(page.text, 'html.parser')
        return page

    def process_text(text):
        text = text.lower()
        text = re.sub('[{}]'.format(string.punctuation), ' ', text)
        text = re.sub('\s+', ' ', text)
        text = re.sub('[a-zA-Z]+[0-9]*', '<UNK>', text)
        text = ' '.join(map(remove_spec_part_from_token, text.split()))
        return text

    page = prepare_page(url_freq_dict)
    words = page.findAll('td')
    dict = {}
    for i in range(15, len(words), 12):
        text = process_text(words[i].text)
        text2 = process_text(words[i + 3].text)
        ch = int(text2.split()[0])
        dict.update({text: ch})
    dict = sorted(dict.items(), key=lambda x: -x[1])
    return dict