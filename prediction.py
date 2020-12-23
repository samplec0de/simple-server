import re
import string

import numpy as np
import requests
import tensorflow as tf


def remove_spec_part_from_token(token):
    for spec_token in ['<NUM>', '<UNK>']:
        if spec_token in token and token != spec_token:
            token = re.sub(spec_token, '', token)
    return token


def process_text(text):
    text = text.text.lower()
    text = re.sub('[{}]'.format(string.punctuation), ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub('\d*[a-zA-Z]+\d*', '<UNK>', text)
    text = re.sub('\d+', '<NUM>', text)
    text = re.sub('\x14|\x15', '', text)
    text = ' '.join(map(remove_spec_part_from_token, text.split()))
    return text


def get_vocab():
    url_train = 'http://lib.ru/LITRA/PUSHKIN/dubrowskij.txt_Ascii.txt'
    url_valid = 'http://lib.ru/LITRA/PUSHKIN/kapitan.txt_Ascii.txt'

    text_train = process_text(requests.get(url_train))
    text_valid = process_text(requests.get(url_valid))

    text_split_train = text_train.split()
    text_split_valid = text_valid.split()

    vocab_train = set(text_split_train)
    vocab_valid = set(text_split_valid)
    vocab = sorted(vocab_train | vocab_valid)

    word2idx = {word: index for index, word in enumerate(vocab)}
    idx2word = np.array(vocab)

    return word2idx, idx2word


def build_model(vocab_size, embedding_dim, rnn_units, batch_size=64):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
        tf.keras.layers.GRU(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)
    ])
    model.load_weights('model.h5')
    model.build(tf.TensorShape([batch_size, None]))
    return model


def generate_text(model, start_string, word2idx, idx2word):
    num_generate = 10
    if start_string not in word2idx:
        print("no such word")
        return start_string
    input_eval = [word2idx[s] for s in start_string.split()]
    input_eval = tf.expand_dims(input_eval, 0)

    text_generated = []

    temperature = 1.0

    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()
        input_eval = tf.expand_dims([predicted_id], 0)
        text_generated.append(idx2word[predicted_id])
    print(len(text_generated))
    return (start_string +' ' + ' '.join(text_generated))
