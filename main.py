from flask import Flask, render_template, request

from Opechatka import *
from prediction import *
import symspell

app = Flask(__name__)

word2idx, idx2word = get_vocab()

model = build_model(len(word2idx), 256, 1024, 1)
symspell.init()


@app.route('/predict', methods=['POST'])
def predict():
    print(request.data.decode())
    return fix_text(request.data.decode())


@app.route('/predict2', methods=['POST'])
def predict2():
    print(request.data.decode())
    return generate_text(model, request.data.decode(), word2idx, idx2word)


@app.route('/predict3', methods=['POST'])
def predict3():
    print(request.data.decode())
    return symspell.solve_with_symspell(request.data.decode())


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
