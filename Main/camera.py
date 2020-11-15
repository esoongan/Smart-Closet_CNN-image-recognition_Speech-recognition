# picamera 설치 후 사용하기
# sudo apt-get install python3-picamera

#from picamera import PiCamera
from time import sleep
import cv2  # opencv 3.4.2+ required
import numpy as np
import matplotlib.pyplot as plt

class CameraModule:

    def capture(self, save_path='../data'):
        '''
        with PiCamera() as picam:
            picam.start_preview()
            sleep(2)
            picam.capture(save_path + '/image.jpg')
            picam.stop_preview()
        '''
        cap =cv2.VideoCapture(0)
        ret,frame = cap.read()
        cv2.imwrite(save_path+'/image.jpg')
        cap.release()

        img = plt.imread(save_path + '/image.jpg')

        '''shape용 이미지'''
        img_shape = cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_LINEAR)
        data_shape = np.asarray(img_shape)
        data_shape = np.array([data_shape])     # 차원 하나 추


        '''pattern용 이미지'''
        h, w, _ = img.shape
        pattern_img = img.copy()
        # 중간부분 크롭한 뒤 resize하기
        cropped_pattern = pattern_img[int(h * 0.25): int(h * 0.75),
                int(w * 0.25): int(w * 0.75)]  # [시작 height : 끝 height, 시작 width : 끝 width]

        cropped_pattern = cv2.resize(cropped_pattern, dsize=(64, 64), interpolation=cv2.INTER_LINEAR)
        data_pattern = np.asarray(cropped_pattern)
        data_pattern = np.array([data_pattern])    # 차원 하나 추가

        return data_pattern, data_shape
