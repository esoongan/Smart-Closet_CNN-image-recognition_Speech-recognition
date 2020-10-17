# -*- coding: utf-8 -*-
"""train_practice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17ao869Gvf_HdK3ySSokebORRIe0LubxQ
"""

from google.colab import drive
drive.mount('/gdrive', force_remount=True)

import os, glob, numpy as np
from keras.models import Model, Sequential
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, Dense, Flatten, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K
import matplotlib.pyplot as plt
import tensorflow as tf

# gpu효율적으로 사용하기 위함 
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

# 각 데이터 형상
# X_train : (훈련데이터갯수, 높이, 너비, 채널수)
# X_test : (시험데이터갯수, 높이, 너비, 채널수)
# y_train : (훈련데이터갯수, 정답클래스 개수)
# y_test : (시험데이터갯수, 정답클래스 개수)

# 이미생성한 .npy파일 불러서 데이터셋 로드 
X_train, X_test, y_train, y_test = np.load('/gdrive/My Drive/졸업프로젝트/ImgData/sample_image_data_npy.npy', None, True)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape) # (213,4) 지맘대로 .DS Store이라는 파일 안에 만들어놔서저럼 ㅂㄷ 
print(y_test.shape)

# 이걸 토대로 층 구성만 다르게하고, 32, 64, 128 다르게해주면서 천천히 하면될거같아!

# 클래스개수 
nb_classes_pattern = 6
nb_classes_shape = 5 

model = Sequential()

# 첫번째 convolutional layer / activation function - 렐루
model.add(Conv2D(32, (3,3), padding="same", input_shape=X_train.shape[1:], activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
    
# 두번째 con
model.add(Conv2D(64, (3,3), padding="same", activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
    
model.add(Conv2D(128, (3,3), padding="same", activation='relu'))
model.add(Conv2D(128, (3,3), padding="same", activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

 # flatten / 출력함수 - 소프트맥수 ( 다중클래스분류에서 주로 사용)
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes_shape, activation='softmax'))

# 손실함수 - 교차엔트로피, optimizer는 adam 으로 하겠다. 
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model_dir = './model'
  
if not os.path.exists(model_dir):
  os.mkdir(model_dir)
  
  model_path = model_dir + '/shape_classification.model'
  checkpoint = ModelCheckpoint(filepath=model_path , monitor='val_loss', verbose=1, save_best_only=True)
  early_stopping = EarlyStopping(monitor='val_loss', patience=6)

model.summary()

# 배치사이즈 얼마로?? 에폭 얼마로?? 
#검증데이터 - 0.2만큼 잘라서 ( 검증데이터는 학습에 이용하지않음, 시험셋으로 테스트하기전에 검증하는용도!! ), 조기종료로 오버피팅 막음 
# 파라미터 설정후 학습 시작! 

history = model.fit(X_train, y_train, batch_size=32, epochs=3, validation_data=(X_test, y_test), callbacks=[checkpoint, early_stopping])

# 위에서 학습된 가중치매개변수의 상태에서 테스트진행 -> 이때는 더이상 갱신은 일어나지않고 그냥 정확도만 평가함. 
print("정확도 : %.4f" % (model.evaluate(X_test, y_test)[1]))

y_vloss = history.history['val_loss']
y_loss = history.history['loss']

x_len = np.arange(len(y_loss))

plt.plot(x_len, y_vloss, marker='.', c='red', label='val_set_loss')
plt.plot(x_len, y_loss, marker='.', c='blue', label='train_set_oss')
plt.legend()
plt.xlabel('epochs')
plt.ylabel('loss')
plt.grid()
plt.show()

from PIL import Image
import os, glob, numpy as np
from keras.models import load_model

caltech_dir = "/gdrive/My Drive/졸업프로젝트/ImgData/shape_test"
image_w = 100
image_h = 100

pixels = image_h * image_w * 3

X = []
filenames = []
files = glob.glob(caltech_dir+"/*.jpg") # png도 하고시프면 *.*로 바꾸면댐!
for i, f in enumerate(files):
    img = Image.open(f)
    img = img.convert("RGB")
    img = img.resize((image_w, image_h))
    data = np.asarray(img)
    filenames.append(f)
    X.append(data)


# 이미지를 행렬로 바꿔서 배욜 X에 저장 
X = np.array(X)
# 학습시킨 모델 가져오기 
model = load_model('./model/shape_classification.model')

# 아까 저장한 배열에 담긴 이미지를 대상으로 예측 
prediction = model.predict(X)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

# 예측값들을 실제 이미지로 테스트해보는코드. 
for num, predict in enumerate(prediction):
  # i 는 [0.000 0.000 0.000 1.000] 의 형태임 
  classes = ["Blazer", "Blouse", "Dress", "LongSleeve", "Pants", "Shirts", "Shorts", "ShortSleeve", "Skirt", "Sleeveless"]
  # 예측값이 0.8이상이면 그게 정답이라고 설정 
  for i, value in enumerate(predict):
    print(i)
    if value >= 0.8:
      print(filenames[num], "이미지는", i, "번째 클래스(", classes[i] ,")로 추정됩니다.")
      break
    else :
      continue

i = [0,0,0,0,1]
classes = ["blzer", "bluse", 'pants','skirt','coat']

for i, value in enumerate(i):
  if value >= 0.8:
    print("해당이미지는",i,"번째 클래스입니다")
    print(classes[i])