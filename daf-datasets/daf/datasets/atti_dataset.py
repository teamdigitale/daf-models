

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ..utils.file_utils import get_file
from ..utils import dataset_utils

import numpy as np
import json

pad_char = 0
start_char = 1
oov_char = 2
index_from = 3


def load_data(path='atti_dataset.npz', num_words=None, skip_top=0, seed=11235):
    """Loads the atti-dirigenti dataset.
    # Arguments
        path: where to cache the data (relative to `~/.keras/dataset`).
        num_words: max number of words to include. Words are ranked
            by how often they occur (in the training set) and only
            the most frequent words are kept
        skip_top: skip the top N most frequently occurring words
            (which may not be informative).
        seed: random seed for sample shuffling.
    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    # Raises

    Note that the 'out of vocabulary' character is only used for
    words that were present in the training set but are not included
    because they're not making the `num_words` cut here.
    Words that were not seen in the training set but are in the test set
    have simply been skipped.
    """
    path = get_file(path,
                    origin='https://media.githubusercontent.com/media/teamdigitale/daf-models/master/daf-datasets/data/atti/{}'.format(
                        path),
                    file_hash='36d64dbf4288c8ba3d30b5180037ed28')

    with np.load(path) as f:
        x_train, labels_train = f['x_train'], f['y_train']
        x_test, labels_test = f['x_test'], f['y_test']

    # shuffle the indices for train and test
    np.random.seed(seed)
    indices = np.arange(len(x_train))
    np.random.shuffle(indices)
    x_train = x_train[indices]
    labels_train = labels_train[indices]

    indices = np.arange(len(x_test))
    np.random.shuffle(indices)
    x_test = x_test[indices]
    labels_test = labels_test[indices]

    if num_words:
        x_train = dataset_utils.filter_dataset(x_train, num_words)
        x_test = dataset_utils.filter_dataset(x_test, num_words)

        # keep non empty columns
        to_keep_train = [i for i in range(len(x_train)) if len(x_train[i]) > 0]
        x_train = x_train[to_keep_train]
        y_train = labels_train[to_keep_train]
        to_keep_test = [i for i in range(len(x_test)) if len(x_test[i]) > 0]
        x_test = x_test[to_keep_test]
        y_test = labels_train[to_keep_test]

    x_all = np.concatenate([x_train, x_test])
    labels_all = np.concatenate([labels_train, labels_test])

    if not num_words:
        num_words = max([max(x) for x in x_all])

    idx = len(x_train)
    x_train, y_train = np.array(x_all[:idx]), np.array(labels_all[:idx])
    x_test, y_test = np.array(x_all[idx:]), np.array(labels_all[:idx])

    return (x_train, y_train), (x_test, y_test)


def get_word_index(path='id_word_dict.json'):
    """Retrieves the dictionary mapping word indices back to words.

    # Arguments
        path: where to cache the data (relative to `~/.daf/dataset`).

    # Returns
        The word index dictionary.
    """
    path = get_file(path,
                    origin='https://media.githubusercontent.com/media/teamdigitale/daf-models/master/daf-datasets/data/atti/{}'.format(
                        path),
                    file_hash='f1c9cb4caa19e5cfc6033c4799bbdc03')
    with open(path, 'r') as f:
        return json.load(f)


def get_label_index(path='label_index.json'):
    """Retrieves the dictionary mapping labels indices back to words.

    # Arguments
        path: where to cache the data (relative to `~/.daf/dataset`).

    # Returns
        The word index dictionary.
    """
    path = get_file(path,
                    origin='https://media.githubusercontent.com/media/teamdigitale/daf-models/master/daf-datasets/data/atti/{}'.format(
                        path),
                    file_hash='bda94d98e9f1771f4131107346a0898f')
    with open(path, 'r') as f:
        return json.load(f)
