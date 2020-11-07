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

    def image_predict(self):
        model = load_model(self.model_dir)

        prediction = model.predict(self.image_processing())
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

        for i, value in prediction:
            classes_pattern = ["줄무늬", '지그재그무늬', '땡땡이', '꽃무늬', '무지', '체크무늬']
            if value >= 0.8:
                result = classes_pattern[i]
                return result

        no_result = '알수없는 패턴'
        return no_result







