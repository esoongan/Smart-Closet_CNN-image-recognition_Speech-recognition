# https://www.dlology.com/blog/how-to-do-hyperparameter-search-with-baysian-optimization-for-keras-model/ 참고
import tensorflow as tf
#from tensorflow.python import keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Dropout, BatchNormalization, MaxPooling2D, Flatten, Activation
import keras.optimizers


# 패턴 총 6개로 분류함
NUM_CLASSES = 6
train_ds = '***train dataset***'
eval_ds = '***evaluate dataset***'
input_shape = '***input shape***'

def get_model(input_shape, dropout2_rate=0.5):
    """Builds a Sequential CNN model to recognize MNIST.

    Args:
      input_shape: Shape of the input depending on the `image_data_format`.
      dropout2_rate: float between 0 and 1. Fraction of the input units to drop for `dropout_2` layer.

    Returns:
      a Keras model

    """
    # Reset the tensorflow backend session.
    # tf.keras.backend.clear_session()
    # Define a CNN model to recognize MNIST.
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape,
                     name="conv2d_1"))
    model.add(Conv2D(64, (3, 3), activation='relu', name="conv2d_2"))
    model.add(MaxPooling2D(pool_size=(2, 2), name="maxpool2d_1"))
    model.add(Dropout(0.25, name="dropout_1"))
    model.add(Flatten(name="flatten"))
    model.add(Dense(128, activation='relu', name="dense_1"))
    model.add(Dropout(dropout2_rate, name="dropout_2"))
    model.add(Dense(NUM_CLASSES, activation='softmax', name="dense_2"))

    print(model.summary())
    return model

# <dense layer의 최적화된 뉴런 개수까지 구하기>
#def fit_with(input_shape, verbose, dropout2_rate, dense_1_neurons_x128, lr):
#     dense_1_neurons = max(int(dense_1_neurons_x128 * 128), 128) ->뉴런 개수는 discrete이므로 int로 바꿔줌: 128, 256, 384
#     model = get_model(input_shape, dropout2_rate, dense_1_neurons)

def fit_with(input_shape, verbose, dropout2_rate, lr):

    # Create the model using a specified hyperparameters.
    # hyperparameters 추가 가능
    model = get_model(input_shape, dropout2_rate)

    # Train the model for a specified number of epochs.
    adam = keras.optimizers.Adam(learning_rate=lr)
    model.compile(loss=tf.keras.losses.categorical_crossentropy,
                  optimizer=adam,
                  metrics=['accuracy'])

    # Train the model with the train dataset.
    # *** epochs, batch_size 조절하기
    model.fit(x=train_ds, epochs=1, steps_per_epoch=None,
              batch_size=64, verbose=verbose)

    # Evaluate the model with the eval dataset.
    # *** steps 조절하기
    score = model.evaluate(eval_ds, steps=10, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    # Return the accuracy.
    # 정확도가 최적화할 타겟임
    return score[1]


from functools import partial
# verbose: 얼마나 상세히 print해 줄 것인지
verbose = 1
fit_with_partial = partial(fit_with, input_shape, verbose)


from bayes_opt import BayesianOptimization
# Bounded region of parameter space
# *** dropout rate와 learning rate의 최적화 실행
# <dense layer의 최적화된 뉴런 개수까지 구하기>
# pbounds = {'dropout2_rate': (0.1, 0.5), 'lr': (1e-4, 1e-2), "dense_1_neurons_x128": (0.9, 3.1)}
pbounds = {'dropout2_rate': (0.1, 0.5), 'lr': (1e-4, 1e-2)}

optimizer = BayesianOptimization(
    f=fit_with_partial,         # fit_with 함수에 대해 최적화
    pbounds=pbounds,
    verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    random_state=1,
)

# init_points: random exploration 횟수-> 탐색 공간을 다양화 할 수 있음
# n_iter: 최적화를 몇 번 할 것인지
optimizer.maximize(init_points=10, n_iter=10,)


for i, res in enumerate(optimizer.res):
    print("Iteration {}: \n\t{}".format(i, res))

print(optimizer.max)