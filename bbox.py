from PIL import Image
import numpy as np
import os

BASE_PATH = "/Users/iseungjin/2020_3_2/capstone/cropImage/newimg"


def crop_image():

    # bbox.txt파일경로
    # 이파일은 파일이름이랑 숫자랑 사이에 공백이 다 달라서 replace하면 안댐.
    filepath = '/Users/iseungjin/2020_3_2/capstone/list_bbox.txt'
    # crop_image 폴더안에는 크롭된 이미지 파일들 28만장 / txt파일 2개
    save_path = '/Users/iseungjin/2020_3_2/capstone/cropImage/'


    f = open(filepath, 'r')

    # 10대신 289222로 변경해야함.
    for i in range(100):
        line = f.readline()
        # image_name = img/Sheer_Pleated-Front_Blouse/img_00000001.jpg
        image_name = line[:line.find(' ')]
        # image_foler = Sheer_Pleated-Front_Blouse
        image_folder = image_name[4:line.rfind('/')]
        # image_number =/img_00000001.jpg
        image_number = image_name[line.rfind('/'):line.rfind('g') + 1]
        print(image_folder + '/'+ image_number)
        # 경계값숫자만 뽑아서 문자열로 먼저 저장.
        image_val = line[71:]
        # 문자열을 배열로 변환
        image_val_list = image_val.split()
        # 문자열 형태의 숫자 정수형 숫자로 바꿔서 배열에저장 - image_val_list_int : [65, 65, 156, 200]
        image_val_list_int = list(map(int, image_val_list))


        #image.open - 이미지 객체를 리턴하는 이미지파일 열어주는 함수.
        # cropImage 폴더 안에 다운받은 img파일 있으면 됨 !!
        image = Image.open('/Users/iseungjin/2020_3_2/capstone/cropImage/' + image_name)
        cropped_image = image.crop(tuple(image_val_list_int))
        # 뭐가 적절한 사이즈일지 잘 모르겠어.. 참고로 28은 개작아 사진
        # cropped_image = cropped_image.resize((100, 100))

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # 저장되는 장소 - '/Users/iseungjin/2020_3_2/capstone/cropImage/newimg/폴더별이름/img_00000001.jpg'
        cropped_image.save(save_path + 'newimg/'+ image_folder + image_number)


os.chdir(BASE_PATH)
crop_image()


#print(pix[100][150]) // 픽셀값 확인

#image.save(crop_image)