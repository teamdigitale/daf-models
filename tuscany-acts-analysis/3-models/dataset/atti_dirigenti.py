import numpy as np
import json

import nltk
from nltk.corpus import stopwords
import string
import os


nltk.download('stopwords')
nltk.download('punkt')

pad_char = 0
start_char = 1
oov_char = 2
index_from = 3

base_path_ = os.path.dirname(os.path.abspath(__file__))

def get_stopwords():
    punctuation = [c for c in string.punctuation]
    punctuation += [',','.','-', '"', "'", ':', ';', '(', ')', '[', ']', '{', '}', '’', '”', '“', '``', "''", '–']
    stop_words = set(stopwords.words('italian'))
    stop_words.update(punctuation)
    return stop_words

def get_labels(path='data_dirigenti_label_index.json'):
    abs_path = '{}/{}'.format(base_path_, path)
    with open(abs_path, 'r') as f:
        label_index = json.load(f)
    return label_index

def get_word_index(path='data_dirigenti_word_index.json'):
    abs_path = '{}/{}'.format(base_path_, path)
    with open(abs_path, 'r') as f:
        word_index = json.load(f)
    return word_index

def get_most_common_words(path='data_dirigenti_most_common.json'):
    abs_path = '{}/{}'.format(base_path_, path)
    with open(abs_path, 'r') as f:
        most_commons = json.load(f)
    return most_commons

def select_indexes_(x,y, idx_words):
    x_new = []
    y_new = []
    for sample,label in zip(x, y):
        # sequence = [ w if w in idx_words else oov_char for w in sample]
        sequence = [ w for w in sample if w in idx_words]
        if not np.all(sequence == oov_char):
            x_new.append(sequence)
            y_new.append(label)
    return x_new, y_new

def load_data(path='data_dirigenti.npz', num_words=None, skip_top=0,
              remove_stopwords=False, seed=11235):
    """Loads the atti-dirigenti dataset.
    # Arguments
        path: where to cache the data (relative to `~/.keras/dataset`).
        num_words: max number of words to include. Words are ranked
            by how often they occur (in the training set) and only
            the most frequent words are kept
        skip_top: skip the top N most frequently occurring words
            (which may not be informative).
        seed: random seed for sample shuffling.
        start_char: The start of a sequence will be marked with this character.
            Set to 1 because 0 is usually the padding character.
        oov_char: words that were cut out because of the `num_words`
            or `skip_top` limit will be replaced with this character.
        index_from: index actual words with this index and higher.
    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_val, y_val), (x_test, y_test)`.
    # Raises

    Note that the 'out of vocabulary' character is only used for
    words that were present in the training set but are not included
    because they're not making the `num_words` cut here.
    Words that were not seen in the training set but are in the test set
    have simply been skipped.
    """
    np.random.seed(seed)

    #add download path from a remote

    #load most_common words
    most_common = get_most_common_words()
    word_index = get_word_index()
    stop_words = get_stopwords()

    if remove_stopwords:
        most_common = [(k,v) for k,v in most_common if k not in stop_words]

    if skip_top > 0:
        most_common = most_common[skip_top:]

    #take only the top k words
    if num_words:
        most_common=most_common[:num_words]


    most_common_selected = set([k for k,v in most_common])

    index_word_selected = { word_index[w]:w for w in most_common_selected}

    abs_path = '{}/{}'.format(base_path_, path)
    with np.load(abs_path) as loaded:
        x_train, y_train = loaded['x_train'], loaded['y_train']
        x_val, y_val = loaded['x_val'], loaded['y_val']
        x_test, y_test = loaded['x_test'], loaded['y_test']

    x_train_new, y_train_new = select_indexes_(x_train, y_train, index_word_selected)
    x_val_new, y_val_new = select_indexes_(x_val, y_val, index_word_selected)
    x_test_new, y_test_new = select_indexes_(x_test, y_test, index_word_selected)

    return most_common_selected, (np.array(x_train_new), np.array(y_train_new)), (np.array(x_val_new), np.array(y_val_new)), (np.array(x_test_new), np.array(y_test_new))
