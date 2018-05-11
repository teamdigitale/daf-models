import numpy as np


def filter_dataset(dataset, top_k):
    # add the pad, end, oov chars
    results = []
    for sequence in dataset:
        results.append([x for x in sequence if x < top_k])
    return np.array(results)


def vectorize_sequences(sequences, dimension):
    results = np.zeros((len(sequences), dimension), dtype=np.float32)
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


def to_one_hot(labels, num_classes):
    results = np.zeros((len(labels), num_classes))
    for i, l in enumerate(labels):
        results[i, l] = 1.
    return results


def dataset_generator_fun(x, y, x_transformer,
                   batch_size, min_index=None, max_index=None, shuffle=False):

    if not min_index:
        min_index = 0
    if not max_index:
        max_index = len(x)

    num_batches = (max_index - min_index) // batch_size + 1
    num_classes = len(set(y))

    i = 0
    while True:
        n = i % num_batches
        i += 1
        if (min_index + (n+1) * batch_size) < max_index:
            # print('then from {} to {}'.format(min_index + n*batch_size, min_index + (n+1)*batch_size))
            yield (
                x_transformer(
                    x[min_index + n*batch_size: min_index + (n+1)*batch_size])(),
                to_one_hot(
                    y[min_index + n*batch_size: min_index + (n+1)*batch_size],
                    num_classes)
            )
        else:
            i = 0
            # print('else from {} to {}'.format(min_index + n*batch_size, max_index))
            yield (
                x_transformer(
                    x[min_index + n*batch_size: max_index])(),
                to_one_hot(
                    y[min_index + n*batch_size: max_index], num_classes
                )
            )
        if shuffle:
            indexes = np.array(range(min_index, max_index))
            np.random.shuffle(indexes)
            x[min_index: max_index] = x[indexes]
            y[min_index: max_index] = y[indexes]

def dataset_generator(x, y, x_dimension,
                   batch_size, min_index=None, max_index=None, shuffle=False):

    if not min_index:
        min_index = 0
    if not max_index:
        max_index = len(x)

    num_batches = (max_index - min_index) // batch_size + 1
    num_classes = len(set(y))

    i = 0
    while True:
        n = i % num_batches
        i += 1
        if (min_index + (n+1) * batch_size) < max_index:
            # print('then from {} to {}'.format(min_index + n*batch_size, min_index + (n+1)*batch_size))
            yield (
                vectorize_sequences(
                    x[min_index + n*batch_size: min_index + (n+1)*batch_size],
                    x_dimension),
                to_one_hot(
                    y[min_index + n*batch_size: min_index + (n+1)*batch_size],
                    num_classes)
            )
        else:
            i = 0
            # print('else from {} to {}'.format(min_index + n*batch_size, max_index))
            yield (
                vectorize_sequences(
                    x[min_index + n*batch_size: max_index],
                    x_dimension),
                to_one_hot(
                    y[min_index + n*batch_size: max_index], num_classes
                )
            )
        if shuffle:
            indexes = np.array(range(min_index, max_index))
            np.random.shuffle(indexes)
            x[min_index: max_index] = x[indexes]
            y[min_index: max_index] = y[indexes]
