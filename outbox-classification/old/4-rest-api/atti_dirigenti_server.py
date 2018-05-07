from keras.models import load_model
import numpy as np
import flask
from flask import request
from dataset import atti_dirigenti
import tensorflow as tf

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('stopwords')
nltk.download('punkt')


# initialize our Flask application and the Keras model
app = flask.Flask(__name__)


def load_model_and_data():
    global word_index
    global label_index
    global index_label
    global model
    # load word index
    word_index = atti_dirigenti.get_word_index()
    # load label index dict
    label_index = atti_dirigenti.get_labels()
    index_label = {v: k for k, v in label_index.items()}

    # load model
    with tf.device('/cpu:0'):
        model = load_model('./weights.07-0.53.hdf5')

    global num_features
    num_features = model.input_shape[-1]


def get_stopwords():
    punctuation = [c for c in string.punctuation]
    punctuation += [',','.','-', '"', "'", ':', ';', '(', ')', '[', ']', '{', '}', '’', '”', '“', '``', "''", '–']
    stop_words = set(stopwords.words('italian'))
    stop_words.update(punctuation)
    return stop_words


stop_words = get_stopwords()


def tokenized_sentence(sample, remove_stopwords=True, tokenizer=word_tokenize):
    words = []
    sample = sample.replace('`', ' ')
    sample = sample.replace("'", " ")
    
    for w in tokenizer(sample):
        if remove_stopwords:
            if w not in stop_words:
                words.append(w.lower())
        else:
            words.append(w.lower())
    return words


def sentece_to_idx(tokenized_sample, max_dimension):
    sequence = []
    for w in tokenized_sample:
        if w in word_index and word_index[w] < max_dimension:
            sequence.append(word_index[w])
        else:
            sequence.append(atti_dirigenti.oov_char)
    return sequence

def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


@app.route('/test', methods = ['GET'])
def test():
    return flask.jsonify({'test': 'success'})


@app.route("/predict", methods = ["POST"])
def predict():
    data = {"success": False}

    try:
        if request.method == 'POST':
            if request.form['sentence']:
                sentence = request.form['sentence']
                tokenized_sentence = tokenize_sample(sentence)
                sequence = sentece_to_idx(tokenized_sentence, num_features)
                vectorized = vectorize_sequences(np.array([sequence]), dimension=num_features)
                with tf.device('/cpu:0'):
                    prediction_prob = model.predict(vectorized)
                # prediction = np.argmax(prediction_prob)
                prediction = index_label[np.argmax(prediction_prob)]

                data['prediction'] = str(prediction)
                data['prediction_probability'] = prediction_prob.tolist()[0]
                data['success'] = True
            else:
                data['message'] = 'missing sentence parameter'
        else:
            data['message'] = 'need to be a post'
    except Exception as e:
        data['message'] = 'got error {}'.format(e.__cause__)

    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_model_and_data()
    app.run()
