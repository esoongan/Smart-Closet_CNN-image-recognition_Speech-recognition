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
        '''각 프로세스에서 리턴값을 큐에 담아야 넘겨받을 수 있음'''
        colorQ = Queue()
        patternQ = Queue()
        shapeQ = Queue()
        # 사진 촬영
        data_pattern, data_shape = self.camera.capture()

        '''각각 프로세스로 만들어서 병렬 처리하게 만들었어 조금이라도 시간을 단축시켜보고자...'''
        # args=('./capture_img/image.jpg')
        color_process = Process(target=color.execute, args=(self.save_path + '/image.jpg', colorQ))
        pattern_process = Process(target=self.pattern.image_predict, args=(data_pattern, patternQ))
        shape_process = Process(target=self.shape.image_predict, args=(data_shape, shapeQ))

        '''프로세스 시작'''
        color_process.start()
        # 카메라모듈에서 전처리된 사진으로 각각 예측하여 스트링 반환.
        pattern_process.start()
        shape_process.start()

        '''프로세스 끝나면 각 큐에서 결과값 추출하기'''
        color_process.join()
        color_string = colorQ.get()

        pattern_process.join()
        pattern = patternQ.get()

        shape_process.join()
        shape = shapeQ.get()

        return color_string, pattern, shape










