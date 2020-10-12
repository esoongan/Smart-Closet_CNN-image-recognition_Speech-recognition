# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from imutils import paths
import argparse
import numpy as np
import os

# os.chdir("/Users/woohyeon/PycharmProjects/keras/1.Data_Augmentation")

# construct the argument parse ad parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-o", "--output", required=True)
ap.add_argument("-p", "--prefix", type=str, default="img")
args = vars(ap.parse_args())


args = {"image": "C:/2020_2/capstone/img_attr/img_attr/animal/img_00000026.jpg", "output": "C:/2020_2/capstone/img_attr/img_attr/auggu", "prefix": "img"}

# image: input 이미지 경로 --> 내가 증폭시키고자 할 이미지 경로!!!
# output: data augmentation의 결과가 저장될 이미지경로 --> 자신에게 맞는 경로로 꼭 수정!!!
# prefix: image filename의 prefix --> img로 통일

print("[INFO] loading example image...")
image = load_img(args["image"])
image = img_to_array(image)
image = np.expand_dims(image, axis=0)  # 맨 앞 1차원 추가

# We are now ready to initialize our ImageDataGenerator:
# construct the image generator for data augmentation then
# initialize the total number of images generated thus far


# ImageDataGenerator가 초기화되면 실제로 새로운 학습 예제를 생성 할 수 있습니다.
aug = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)


# 증강 이미지를 구성하는 데 사용되는 Python 생성기를 초기화합니다. 출력 이미지 파일 경로, 각 파일 경로의 접두사 및 이미지 파일 형식을 지정하기 위한
# 몇 가지 추가 매개 변수와 함께 입력 이미지 인 batch_size 1을 전달합니다 (하나의 이미지 만 증가 시키므로).
print("[INFO] generating images...")
imageGen = aug.flow(
    image,
    batch_size=1,
    save_to_dir=args["output"],
    save_prefix=args["prefix"],
    save_format="jpg",
)

total = 0
# 그런 다음 imageGen 생성기의 각 이미지를 반복하기 시작합니다. 내부적으로 imageGen은 루프를 통해 요청 될 때마다 새로운 학습 샘플을 자동으로 생성합니다.
# 그런 다음 디스크에 기록 된 총 데이터 증가 예제 수를 늘리고 예제 10 개에 도달하면 스크립트 실행을 중지합니다.
# loop over examples from our image data augmentation generator
for image in imageGen:
    # increment our counter
    total += 1

    # if we have reached 10 examples, break from the loop
    if total == 10:
        break