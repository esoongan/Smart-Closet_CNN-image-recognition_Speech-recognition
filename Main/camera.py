# picamera 설치 후 사용하기
# sudo apt-get install python3-picamera

from picamera import PiCamera
from time import sleep
import cv2  # opencv 3.4.2+ required
import numpy as np
import matplotlib.pyplot as plt

class CameraModule:
    def __init__(self):
        self.picam = PiCamera()
        self.picam.rotation = 180
        # 밝기 70으로 설정
        # camera.brightness = 70

    def capture(self, save_path='.'):
        self.picam.start_preview()
        # 2초후 캡쳐
        sleep(2)
        self.picam.capture(save_path + '/image.jpg')
        self.picam.stop_prview()

        img = plt.imread(save_path + '/image.jpg')

        '''shape용 이미지'''
        img_shape = cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_LINEAR)
        data_shape = np.asarray(img_shape)

        '''patter용 이미지'''
        img_pattern = cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_LINEAR)
        # img_size[0] = 높이, img_size[1] = 너비, img_size[2] = 채널
        img_size = img.shape
        img_h_middle = int(img_size[0] / 2)
        img_w_middle = int(img_size[1] / 2)

        # 패턴이니까 중간부분으로 자르기
        cropped_pattern = img[img_h_middle - 32:img_h_middle + 32, img_w_middle - 32:img_w_middle + 32]

        cropped_pattern = cv2.resize(cropped_pattern, dsize=(64, 64), interpolation=cv2.INTER_LINEAR)
        data_pattern = np.asarray(cropped_pattern)

        return data_pattern, data_shape
