from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.callbacks import TensorBoard

# parameters
model_name = 'model1'
batch_size = 10
width = 26  # mfcc features
max_utr_len = 200  # (max) length of utterance
features_dim = 26
classes = 13  # activities
epochs_num = 100

X_train = X
Y_train = Y
X_test = X
Y_test = Y

print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(max_utr_len, features_dim)))
model.add(Dense(classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model.fit(X_train, Y_train,
          nb_epoch=epochs_num,
          batch_size=batch_size,
          shuffle=True,
          validation_data=(X_train, Y_train),
          callbacks=[TensorBoard(log_dir='/lstm/' + model_name)])

model.evaluate(X_test, Y_test, batch_size=13, verbose=1, sample_weight=None)