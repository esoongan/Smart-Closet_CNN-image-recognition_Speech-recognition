import numpy as np
from tensorflow import keras

# from patternNN import pattern
# pattern = pattern()
# pattern.model_predict() --> ~무늬 혹은 알수없는 패턴 리턴.

class Pattern:

    def __init__(self):
        #self.img_dir = "'../data'"
        self.model_dir = "../data/olddata_pattern_load_vgg.h5"

    # img 파라미터 추가 -> classification에서 camera.capture()의줌 리턴값(data_pattern)을 여기 넣어
    def image_predict(self, img, q):
        #model = load_model(self.model_dir)
        model = keras.models.load_model(self.model_dir)

        prediction = model.predict(img)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

        index = 0
        for value in prediction[0]:
            # final data로 만든 신경망은 클래스 순서 다른 거 주의하기
            classes_pattern = ["줄무늬", '지그재그무늬', '땡땡이', '꽃무늬', '무지', '체크무늬']
            if value >= 0.8:
                result = classes_pattern[index]
                q.put(result)
                return result
            index = index+1

        no_result = ''       # -> 그냥 아무것도 출력 안하거나 '무늬가 있는' 이런 식으로 뭉뜽그리는게 더 낫지 않을까??
        q.put(no_result)
        return no_result







