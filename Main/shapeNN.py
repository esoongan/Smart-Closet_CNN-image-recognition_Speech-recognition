from PIL import Image
import os, glob, numpy as np
from keras.models import load_model


class Shape:

    def __init__(self):
        #self.img_dir = "'../data'"
        self.model_dir = "../data/shape_model.h5"

    def image_predict(self, img, q):
        model = load_model(self.model_dir)

        prediction = model.predict(img)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

        for i, value in prediction:
            classes_shape = ["반팔", "블레이저", "원피스", "셔츠", "블라우스", "민소매", "반바지", "치마", "긴팔", "긴바지"]
            if value >= 0.8:
                result = classes_shape[i] # 입니다. 붙여서 최종출력.
                q.put(result)
                return result

        no_result = '옷'     # '빨간색 꽃무늬 알 수 없는 옷 입니다.' -> '빨간색 꽃무늬 옷입니다.' 이게 더 나을 거같아서 변경했어
        q.put(no_result)
        return no_result







