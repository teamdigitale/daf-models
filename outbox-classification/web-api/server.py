import tensorflow as tf
import numpy as np
import flask
from flask import request
from flask_cors import CORS
import os
import json

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

nltk.download('stopwords')
nltk.download('punkt')

pad_char = 0
start_char=1
oov_char=2

tokenizer = RegexpTokenizer(r'\w+')

def load():
    """ load the model and all the dictionary need

    """
    global word_id_dict, id_label_dict, num_words, stop_words, model

    punctuation = ['-', '"', "'", ':', ';', '(', ')', '[', ']', '{', '}', '’', '”', '“', '``', "''"]
    stop_words = set(stopwords.words('italian'))
    stop_words.update(punctuation)

    with open('./data/id_word_dict.json', 'r') as f:
        id_word_dict = json.load(f)
        word_id_dict = {v:int(k) for k,v in id_word_dict.items()}

    with open('./data/label_index.json', 'r') as f:
        label_id_dict = json.load(f)
        id_label_dict = {v: k for k, v in label_id_dict.items()}

    with tf.device('/cpu:0'):
        model = tf.keras.models.load_model('./data/dropout_model.hdf5')
        model._make_predict_function()
        print(model.summary())

    num_words = model.input_shape[-1]


def hasnumbers(value):
    return any(c.isdigit() for c in value)


def tokenize_sentence(sentence, remove_stopwords=True, tokenizer=tokenizer.tokenize):
    """
    Tokenize the sentence and remove stopwords if true
    :param sentence: the sentence to be tokenized
    :param remove_stopwords: True to remove stopwa
    :param tokenizer:
    :return:
    """
    sentence = sentence.replace('`', ' ')
    sentence = sentence.replace("'", " ")
    sentence = sentence.replace("”", ' ')
    sentence = sentence.replace("“", ' ')
    words = []

    for w in tokenizer(sentence):
        if not hasnumbers(w) and len(w) > 2:
            w = w.replace('_', '')
            if remove_stopwords:
                if w not in stop_words:
                    words.append(w.lower())
            elif w in stop_words or len(w) > 1:
                words.append(w.lower())
    yield words


def sentence_to_idxs(tokenized_sentence):
    """
    convert a tokenized sentence into a sequence of idx
    :param tokenized_sentence:
    :param max_idx:
    :return:
    """
    results = []
    for sample in tokenized_sentence:
        encoded_sample = []
        for w in sample:
            if w in word_id_dict:
                encoded_sample.append(word_id_dict[w])
            else:
                encoded_sample.append(oov_char)
        results.append(encoded_sample)
    return results


def vectorize_sequences(sequences, num_words):
    """

    :param sequences:
    :param dimension:
    :return: sequences encoded as indicator arrays
    """
    results = np.zeros((len(sequences), num_words))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


def sentence_pipeline(sentence):
    """
    :param sentence:
    :return: the sentence into its vectorized form
    """
    tokenized = list(tokenize_sentence(sentence))
    sequence = list(sentence_to_idxs(tokenized))
    vectorized = vectorize_sequences([sequence], num_words)
    return vectorized


# create the app
app = flask.Flask("api-server", static_folder='public')
CORS(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("public" + path):
        return flask.send_from_directory('public/', path)
    else:
        return flask.send_from_directory('public', 'index.html')


@app.route('/healtz', methods=['GET'])
def healtz():
    return flask.jsonify({'healtz': 'ok'})


@app.route('/predict', methods=['POST'])
def predict():
    data = {'success': False}
    content = request.get_json()
    try:
        if content:
            if 'sentence' in content:
                sentence = content['sentence']
                vectorized = sentence_pipeline(sentence)
                with tf.device('/cpu:0'):
                    predictions = model.predict(vectorized)

                predictions_dict = {id_label_dict[i]: "{:.10f}".format(v) for i, v in enumerate(predictions[0]) if i in id_label_dict}

                predicted_class = np.argmax(predictions)

                data['prediction'] =  str(id_label_dict[predicted_class])
                data['prediction_prob'] = "{:.10f}".format(predictions[0, predicted_class])[:5]
                data['prediction_probabilities'] = predictions_dict
                data['success'] = True
            else:
                data['message'] = 'missing sentence parameter'
        else:
            data['message'] = 'missing body'

    except Exception as e:
        data['message'] = 'got error {}'.format(e)

    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load()
    app.run(debug=False, host='0.0.0.0')
