from PIL import Image
import os, glob, numpy as np
from keras.models import load_model

# from patternNN import pattern
# pattern = pattern()
# pattern.model_predict() --> ~무늬 혹은 알수없는 패턴 리턴.

class pattern:

    def __init__(self):
        self.img_dir = "'../data'"
        self.model_dir = "../data/pattern_model.h5"
        self.image_w = 64
        self.image_h = 64

    def image_processing(self):
        img = self.img_dir + "/image.jpg"
        img = Image.open(img)
        img = img.convert("RGB")
        img = img.resize((self.image_w, self.image_h))
        img = np.asarray(img)
        return img

    def model_predict(self):
        model = load_model(self.model_dir)

        prediction = model.predict(self.image_processing())
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

        for i, value in prediction:
            classes_pattern = ["줄", '지그재그', '땡땡이', '꽃', '기본', '체크']
            if value >= 0.8:
                result = classes_pattern[i] + "무늬"
                return result

        no_result = '알수없는 패턴'
        return no_result







