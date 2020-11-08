from PIL import Image
import os, glob, numpy as np
from keras.models import load_model

# from patternNN import pattern
# pattern = pattern()
# pattern.model_predict() --> ~무늬 혹은 알수없는 패턴 리턴.

class Pattern:

    def __init__(self):
        #self.img_dir = "'../data'"
        self.model_dir = "../data/pattern_model.h5"

    # img 파라미터 추가 -> classification에서 camera.capture()의줌 리턴값(data_pattern)을 여기 넣어
    def image_predict(self, img, q):
        model = load_model(self.model_dir)

        # 여기 클래스에는 image_processing 함수가 없는데 이거 뭐야?? -하영
        # prediction = model.predict(self.image_processing())
        prediction = model.predict(img)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

        for i, value in prediction:
            classes_pattern = ["줄무늬", '지그재그무늬', '땡땡이', '꽃무늬', '무지', '체크무늬']
            if value >= 0.8:
                result = classes_pattern[i]
                q.put(result)
                return result

        no_result = '알수없는 패턴'       # -> 그냥 아무것도 출력 안하거나 '무늬가 있는' 이런 식으로 뭉뜽그리는게 더 낫지 않을까??
        q.put(no_result)
        return no_result







