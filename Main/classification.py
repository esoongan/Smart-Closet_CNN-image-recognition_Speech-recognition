from multiprocessing import Process, Queue
import color as color
from camera import CameraModule
from patternNN import Pattern
from shapeNN import Shape

class Classification:
    def __init__(self):
        '''
               shapeNN, patternNN = 인스턴스 생성
               colorDetector = 클래스 인스턴스 생성
         '''
        self.camera = CameraModule()
        self.pattern = Pattern()
        self.shape = Shape()


    def execute(self):
        colorQ = Queue()
        # 사진 촬영
        data_pattern, data_shape = self.camera.capture()

        # args=('./capture_img/image.jpg')
        color_process = Process(target=color.execute, args=(self.save_path + '/image.jpg', colorQ))
        color_process.start()

        color_process.join()
        color_string = colorQ.get()

        # 카메라모듈에서 전처리된 사진으로 각각 예측하여 스트링 반환.
        pattern = self.pattern.image_predict(data_pattern)
        shape = self.shape.image_predict(data_shape)

        return color_string, pattern, shape










