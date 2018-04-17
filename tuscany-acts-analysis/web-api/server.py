from keras.models import load_model
import numpy as np
import flask
from flask import request
from flask_cors import CORS
from dataset import atti_dirigenti
import tensorflow as tf
import os

import nltk
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')


def load():
    """ load the model and all the dictionary need

    """
    global word_index, label_index, index_label, model, num_features, stop_words
    word_index = atti_dirigenti.get_word_index()
    label_index = atti_dirigenti.get_labels()
    index_label = {v: k for k, v in label_index.items()}

    stop_words = atti_dirigenti.get_stopwords()

    with tf.device('/cpu:0'):
        model = load_model('./model.hdf5')

    num_features = model.input_shape[-1]


def tokenize_sentence(sentence, remove_stopwords=True, tokenizer=word_tokenize):
    """
    Tokenize the sentence and remove stopwords if true
    :param sentence: the sentence to be tokenized
    :param remove_stopwords: True to remove stopwa
    :param tokenizer:
    :return:
    """
    sentence = sentence.replace('`', ' ')
    sentence = sentence.replace("'", " ")

    for word in tokenizer(sentence):
        if remove_stopwords:
            if word not in stop_words:
                yield word.lower()
        else:
            yield word.lower()


def sentence_to_idxs(tokenized_sentence, max_idx):
    """
    convert a tokenized sencente into a sequence of idx
    :param tokenized_sentece:
    :param max_idx:
    :return:
    """
    for w in tokenized_sentence:
        if w in word_index and word_index[w] < max_idx:
            yield word_index[w]
        else:
            yield atti_dirigenti.oov_char


def vectorize_sequences(sequences, dimension):
    """

    :param sequences:
    :param dimension:
    :return: sequences encoded as indicator arrays
    """
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


def sentence_pipeline(sentence):
    """
    :param sentence:
    :return: the sentence into its vectorized form
    """
    tokenized = list(tokenize_sentence(sentence))
    sequence = list(sentence_to_idxs(tokenized, num_features))
    vectorized = vectorize_sequences([sequence], num_features)
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

                predictions_dict = {index_label[i]: "{:.10f}".format(v) for i, v in enumerate(predictions[0])}

                predicted_class = np.argmax(predictions)

                data['prediction'] =  str(index_label[predicted_class])
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
