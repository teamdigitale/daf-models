
# coding: utf-8

# In[1]:


import numpy as np
import random
from dataset import atti_dirigenti

from keras import layers, models, optimizers, utils, metrics
from keras.callbacks import *
from keras.wrappers.scikit_learn import KerasClassifier
from keras.models import load_model
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

from scipy import stats


# In[2]:


(x_train, y_train),(x_val, y_val), (x_test, y_test) = atti_dirigenti.load_data(num_words=5000, remove_stopwords=True)


# In[3]:


x_train[:5]


# In[4]:


label_index = atti_dirigenti.get_labels()
len(label_index)


# In[5]:


num_classes = len(label_index)


# In[6]:


def max_index(data):
    return max(data.max())


# In[7]:


max_idx = max([max_index(x_train), max_index(x_val), max_index(x_test)]) + 10


# In[8]:


max_idx


# In[9]:


num_features = max_idx 


# In[10]:


def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


# In[11]:


def vectorize_sequences_generator(sequences, dimension, batch_size):
    num_batches = len(sequences) // batch_size
    
    i=0
    while True:
        # to be sure don't go over the size of the dataset
        n = i % num_batches
        i +=1
        if (n+1) * batch_size < len(sequences):
            yield vectorize_sequences(sequences[n*batch_size : (n+1)*batch_size], dimension)
        else:
            yield vectorize_sequences(sequences[n*batch_size : len(sequences)], dimension)


# #### Evaluate if works

# In[12]:


batch_size = 256
steps_per_epoch = len(x_train) // batch_size

i = 0
for batch in vectorize_sequences_generator(x_train, num_features, batch_size):
    print(np.argmax(batch[-1]))
    i+=1
    
    if i == 10:
        break
    


# In[13]:


batch_size = 256


# In[14]:


def to_one_hot(labels, num_classes):
    results = np.zeros((len(labels), num_classes), dtype=np.float16)
    for i, label in enumerate(labels):
        results[i, label] = 1.
    return results


# In[15]:


def to_one_hot_generator(labels, batch_size, num_classes):
    num_batches = len(labels) // batch_size
    num_classes = len(set(labels))
    
    i = 0
    while True:
        n = i % num_batches
        i += 1
        if (n+1) * batch_size < len(labels):
            yield to_one_hot(labels[n*batch_size : (n+1)*batch_size], num_classes)
        else:
            yield to_one_hot(labels[n*batch_size : len(labels)], num_classes)
        


# In[16]:


batch_size = 256
steps_per_epoch = len(y_train) // batch_size

i = 0
for batch in to_one_hot_generator(y_train, batch_size, num_classes):
    for v in batch[:10]:
        print(np.argmax(v))
    break

    


# In[17]:


y_train[:10]


# In[18]:


def data_generator(data, labels, batch_size, num_features, num_classes):
    x_generator = vectorize_sequences_generator(data, num_features, batch_size)
    y_generator = to_one_hot_generator(labels, batch_size, num_classes)
    
    while True:
        yield next(x_generator), next(y_generator)


# In[19]:


for x_batch, y_batch in data_generator(x_train, y_train, 256, num_features, num_classes):
    print(x_batch.shape, y_batch.shape)
    break


# In[21]:


train_generator = data_generator(x_train, y_train, batch_size, num_features, num_classes)
val_generator = data_generator(x_val, y_val, batch_size, num_features, num_classes)
test_generator = data_generator(x_test, y_test, batch_size, num_features, num_classes)


# ### Dataset for hyper parameters optimization

# In[20]:


size = int(len(x_train) * 0.4)


# In[21]:


x_train_grid = vectorize_sequences(x_train[0:size], num_features)
y_train_grid = to_one_hot(y_train[0:size], num_classes)


# #### Evaluate if works

# ### Build the Model

# In[22]:


def build_model(neurons, dropout, num_features, num_classes, activation='relu', init_mode='glorot_uniform'):
    input_tensor = layers.Input(shape=(num_features,))
    first_layer = True
    for n in neurons:
        if first_layer:
            first_layer = False
            l = layers.Dense(n, activation=activation, kernel_initializer=init_mode)(input_tensor)
            l = layers.Dropout(dropout)(l)
        else:
            l_next = layers.Dense(n, activation=activation, kernel_initializer=init_mode)(l)
            l_next = layers.Dropout(dropout)(l_next)
            l = l_next
    last_layer = layers.Dense(num_classes, activation='softmax')(l)
    model = models.Model(inputs = [input_tensor], outputs = [last_layer])
    
    model.compile(loss='categorical_crossentropy', optimizer= 'Adam', metrics=['accuracy'])
    return model


# ### Search for the best parameters

# In[25]:


wrapped_model = KerasClassifier(build_fn=build_model, num_features=num_features, num_classes=num_classes)


# In[26]:


# neurons = sorted(np.random.randint(0,128,(5,1)))
# dropout = sorted(np.random.rand(5))
base = [16,64,128]
neurons = [[x] for x in base]
neurons += [[x,x] for x in base]
neurons += [[x,x,x] for x in base]
dropout = np.arange(0.1, 0.7, step=0.1)
activation = ['relu', 'tanh', 'sigmoid']
init_mode = ['uniform', 'lecun_uniform', 'normal', 'glorot_normal']


# In[27]:


param_dist = dict(neurons=neurons, dropout=dropout, activation=activation)


# In[28]:


grid = GridSearchCV(wrapped_model, param_grid=param_dist)


# In[ ]:


grid_result= grid.fit(X=x_train_grid, y=y_train_grid)


# ### Summarize Results

# In[1]:


# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

