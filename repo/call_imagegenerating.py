# coding=utf-8
import os

# FOLDERS_PATH: 이름이 <속성>인 폴더들이 있는 경로
FOLDERS_PATH = '/Users/hayeong/Downloads/generating'
# OUTPUT_PATH: 새로운 폴더들이 생길 경로
OUTPUT_PATH = '/Users/hayeong/Downloads'
# PROGRAM_PATHimagegenerating.py가 있는 경로
PROGRAM_PATH = '/Users/hayeong/Smart-Closet/repo'
os.system('cd '+PROGRAM_PATH)

# category_dirs: list[blouse, tank, dress, ...]
category_dirs = os.listdir(FOLDERS_PATH)
category_dirs.pop(category_dirs.index('.DS_Store'))
for category in category_dirs:
    # input_list: list[img_1.jpg, img_4.jpg, ...]
    input_list = os.listdir(FOLDERS_PATH+'/'+category)
    for image in input_list:
        input_arg = FOLDERS_PATH+'/'+category+'/'+image
        newpath = input_arg.replace(' ', '')
        os.rename(input_arg, newpath)

        # output 폴더 생성
        output_arg = OUTPUT_PATH+'/'+category
        if not os.path.exists(output_arg):
            os.makedirs(output_arg)
        
        # image: input 이미지 경로 --> 내가 증폭시키고자 할 이미지 경로!!!
        # output: data augmentation의 결과가 저장될 이미지경로 --> 자신에게 맞는 경로로 꼭 수정!!!
        # prefix: image filename의 prefix --> img로 통일
        # args = {"image": input_arg, "output": output_arg, "prefix": "img"}
        os.system('python imagegenerating.py -i ' + newpath + ' -o ' + output_arg)
