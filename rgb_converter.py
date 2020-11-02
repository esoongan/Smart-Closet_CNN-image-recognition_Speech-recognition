# 이거 대신 lab_converter 사용하기!!!
import numpy as np


### 색상간 거리를 계산하여 가장 비슷한(거리가 가까운) 색상명으로 맵핑해주는 프로그램
# 사용할 색상 카테고리를 얼마나 세분화할 지 고민해보아야 함
class RGBconverter:

    def __init__(self, colors_path = '/Users/hayeong/Smart-Closet/color-rgb.txt'):
        # {'name': <색상 이름>, 'rgb': [r, g, b]}를 원소로 갖음
        # 사전에 정의한 색상 이름과 rgb를 dictionary로 묶어서 color_list에 저장
        # format: <색상명> <r>,<g>,<b>
        # line[0]: 빨간색 185,32,33
        self.COLORS_FILE_PATH = colors_path
        self.color_list = []
        self.init_color_list()



    # format: <색상명> <r>,<g>,<b>
    # ex) line[0]: 빨간색 185,32,33
    def set_path(self, path):
        self.COLORS_FILE_PATH = path

    def init_color_list(self):
        f = open(self.COLORS_FILE_PATH, 'r')
        while (True):
            line = f.readline()
            if line == '':
                break
            if line == '\n':
                continue
            # preprocessing
            color_name = line[:line.find('/')]  # -> '빨강' / '주황' / ...
            rgb = line[line.find(' ') + 1:].split(',')  # -> [255, 0, 0]

            # str list -> int list
            rgb = list(map(int, rgb))

            color_dict = {'name': color_name, 'rgb': rgb}
            self.color_list.append(color_dict)
        f.close()

    def get_color_list(self):
        return self.color_list

    # rgb간 거리 계산 함수
    # 이 거리가 가장 작은 (미리 정의된)색상으로 맵핑한다.
    def distance(self, rgb1, rgb2):
        return np.sqrt((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2)

    # rgb간 거리를 계산하여 가장 가까운 거리의 (미리 정의된)색상으로 맵핑해준다.
    # rgb: 미리 정의된 색상으로 맵핑 할 원래 rgb값
    def rgb_to_name(self, rgb):
        min_d = 987654321
        index = -1

        # 최솟값(min_d)과 최솟값이 위치하는 인덱스(index) 구함
        for i in range(len(self.color_list)):
            d = self.distance(rgb, self.color_list[i]['rgb'])
            if d < min_d:
                min_d = d
                index = i
        # 가장 근접한 색상명 리턴
        return self.color_list[index]['name']
