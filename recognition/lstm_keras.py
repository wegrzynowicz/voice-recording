import numpy as np
import json
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers.recurrent import LSTM
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeavePGroupsOut
from keras.callbacks import TensorBoard


# Model parameters
batch_size = 20
hidden_units = 75
nb_classes = 14
nb_epoch = 250
model_name = 'model'
user_indep = True

# Data loading and spliting
print('Loading data...')
f = np.load('features.npz')
X = f['X']
Y =f['Y']
labels = f['labels']
unique_labels = list(set(labels))
unique_labels.append('Nieznany')
people = f['people']
if user_indep:
    lpgo = LeavePGroupsOut(n_groups=3)
    lpgo.get_n_splits(X, Y, people)
    for train_index, test_index in lpgo.split(X, Y, people):
        X_train, X_test = X[train_index,:,:], X[test_index,:,:]
        y_train, y_test = Y[train_index], Y[test_index]
        break
else:
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42,stratify=Y)
y_train = np_utils.to_categorical(y_train, nb_classes)
y_test = np_utils.to_categorical(y_test, nb_classes)

# Model compilation
print('Build model...')
model = Sequential()
model.add(LSTM(output_dim=hidden_units, init='uniform', inner_init='uniform',
               forget_bias_init='one', activation='tanh', inner_activation='sigmoid', input_shape=X_train.shape[1:], return_sequences=False))
model.add(Dense(nb_classes,activation='softmax'))
board=TensorBoard(log_dir='/tmp/' + model_name, histogram_freq=5, write_graph=True, write_images=False)
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

# Training model
print("Train model...")
model.fit(X_train, y_train,
          batch_size=batch_size,
          nb_epoch=nb_epoch,
          validation_data=(X_test, y_test),
          callbacks=[board])

# Testing model
loss,score = model.evaluate(X_test, y_test, batch_size=batch_size)
print('\nTest score: %.2f%%, Loss: %.2f' % (score*100,loss))

# Saving model:
with open("models/"+model_name+".json", "w") as json_file:
    json_file.write(model.to_json())
np.savez("models/labels.npz",labels = unique_labels)
# serialize weights to HDF5
model.save_weights("models/"+model_name+".h5")
print("Saved model to disk")