import numpy as np
from tensorflow import keras


class Shape:

    def __init__(self):
        #self.img_dir = "'../data'"
        # model 저장된 경로 넣으셈!!
        self.model_dir = "../data/.h5"

    def image_predict(self, img, q):
        ''' 테스트 하라고 주석 처리해논거야 옷 종류도 인식하려면 이 부분 주석 처리 없애고 model_dir에 shape 모델만 넣으면 됨!
        #model = load_model(self.model_dir)
        model = keras.models.load_model(self.model_dir)
        prediction = model.predict(img)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

        index = 0
        for value in prediction[0]:
            classes_shape = ["반팔", "블레이저", "원피스", "셔츠", "블라우스", "민소매", "반바지", "치마", "긴팔", "긴바지"]
            if value >= 0.8:
                result = classes_shape[index] # 입니다. 붙여서 최종출력.
                q.put(result)
                return result
            index = index+1
        '''

        no_result = '옷'
        q.put(no_result)
        return no_result







