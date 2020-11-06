from multiprocessing import Process, Queue
import color as color
from camera import CameraModule

class Classification:
    def __init__(self):
        self.camera = CameraModule()
        '''
        shapeNN = 모델 불러오기
        patternNN = 모델 불러오기
        colorDetector = 클래스 인스턴스 생성
        '''

    def execute(self):
        colorQ = Queue()
        # 사진 촬영
        data_pattern, data_shape = self.camera.capture()

        # args=('./capture_img/image.jpg')
        color_process = Process(target=color.execute, args=(self.save_path + '/image.jpg', colorQ))
        color_process.start()

        color_process.join()
        color_string = colorQ.get()

        return color_string




