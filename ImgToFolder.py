import os
import shutil

# 속성 개수
ATTR_SIZE = 1000
CATEGORY_SIZE = 50

# 새 폴더들이 생성될 곳의 부모 경로
# -----BASE_PATH 폴더에 있어야 할 것들-----
# 1. img 폴더 : DeepFashion DB의 오리지날 img 폴더(폴더 옮길 이미지 파일들)
# 2. list_attr_img.txt
# 3. list_attr_cloth.txt
BASE_PATH = "/Users/iseungjin/2020_3_2/test"

# 지영언니가 만든 각 사진별 속성값이 적혀있는 텍스트 파일 경로 (신경망 별로 이 경로를 변경하여 프로그램 실행)
attr_img_path = "./test_list_attr_img.txt"
cate_img_path = "./list_category_img.txt"
# 우리가 추린 속성들 리스트가 담긴 텍스트 파일 경로
attr_path = './test_list_attr_cloth.txt'
cate_path = './list_category_cloth.txt'



# !!한 이미지에 두 개 이상 속성이 있으면 처음 나온 속성에 따라서만 이동됨

# folder_name: 해당 이미지에 속한 속성 이름으로 폴더명이 됨
# img_name: list_attr_img의 각 행 첫부분에 해당하는 문자열    ex) img/Sheer_Pleated-Front_Blouse/img_00000001.jpg
def moveToFolder(folder_name, img_name, n):
    # folder_name 폴더가 없으면 생성
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print('===[' + folder_name + ']' + ' has been created.')

    # 여기서 './'은 BASE_PATH임
    # 속성 이름으로 된 폴더의 경로 (이동할 곳)
    dest_path = "./" + folder_name

    # 이미지의 원래 있던 폴더의 경로 (DeepFashion DB의 img폴더 위치)
    src_path = './' + img_name

    # 이미지 파일의 이름 형식: img_00000001, img_00000002, ...
    # 그냥 폴더에 옮겨진 순서대로 번호가 매겨짐
    # (원래는 폴더별로 1부터 시작하지만 이런식으로 하려면 파일 개수 일일이 세야해서 과부하 위험 있음)
    new_img_name = '/img_' + format(n, '08')+'.txt'         # .txt -> jpg로 바꿔야함

    # 파일 이름을 위의 new_img_name으로 변경하고 속성별 폴더로 이동시키기
    shutil.move(src_path, dest_path+new_img_name)
    print('[' + img_name +']: '+src_path+' -----> '+dest_path+new_img_name)
    print()
    return


# make_attrlist와 같은 기능을 함
def make_categorylist():
    categories = open(cate_path, 'r')

    # list_category_img.txt에서 index가 1부터 시작함
    catelist = ['null']

    for i in range(CATEGORY_SIZE):
        # 한 줄에 공백 없는 카테고리 이름만 적혀있다고 가정함
        # ex) line1: 'pants         2' line2: 'skirt         2'
        line = categories.readline()
        category = line[:line.find(' ')]
        catelist.append(category)

    # category[index] = <카테고리 이름>
    return catelist


# list_category_cloth로 폴더 나누기
def cate_main():
    f= open(cate_img_path, 'r')

    catelist = make_categorylist()
    n = 0
    while(True):

        # ex) line1: img/<폴더 이름>/<사진 이름>.jpg               31 (
        line = f.readline()
        img_name = line[:line.find(' ')]
        img_cate = line[line.rfind(' ')+1:]

        folder_name = catelist[int(img_cate)]
        moveToFolder(folder_name, img_name, n)
        n = n+1






def attr_main():
    f = open(attr_img_path, 'r')

    # attrlist[index] = <속성 이름>
    attrlist = make_attrlist()

    # n은 이미지 파일이 폴더에 각각 옮겨질 때 파일의 이름에 들어가서 일련번호 같은 역할을 할 것임
    n = 0
    while (True):

        # list_attr_img.txt 파일 불러오기
        line = f.readline()

        # 파일 끝까지 읽었을 때 break
        if line == '':
            break;

        # 승진 언니코드랑 똑같음 (문자열 파싱, 속성값들을 리스트로 만듬)
        line = line.replace("                        ", ",")
        img_name = line[:line.find(',')]

        image_val = line[line.find(',') + 1:]
        image_val_list = image_val.split()

        # attrlist의 인덱스로 쓰임으로써 속성값이 '1'인 속성 이름을 추출함
        index = 0
        for i in range(ATTR_SIZE):
            if image_val_list[i] == '1':
                index = i
                break

        # 이미지 속성값에서 '1'을 찾지 못했을 때
        if i >= ATTR_SIZE-1:
            print('***'+img_name + ' 속성값이 없습니다.')
            continue

        # 속성값이 '1'인 곳의 index로 속성 이름을 가져오고 이를 목적지 폴더명으로 사용
        folder_name = attrlist[index]

        # folder_name: 목적지 폴더
        # img_name: 해당 이미지의 경로 ex) img/<폴더 이름>/<사진 이름>.jpg
        # n: 이미지 파일의 새 이름에 들어갈 일련번호
        moveToFolder(folder_name, img_name, n)
        n = n+1


# 각 속성값을 인덱스로 접근할 수 있는 리스트를 리턴함
# attr_path: 사용할 속성 리스트가 있는 텍스트 파일 경로
# attr_img_path: 지영언니가 만든 각 사진별 속성값이 적혀있는 텍스트 파일 경로
def make_attrlist():
    attrs = open(attr_path, 'r')
    attrlist = []

    for i in range(ATTR_SIZE):
        # 한 줄에 공백 없는 속성 이름만 적혀있다고 가정함
        # ex) line1: 'check', line2: 'stripe'
        attr = attrs.readline()
        attr = attr[:-1]

        # attrlist[index] = <속성 이름> 으로 저장
        # 이 <속성 이름>이 폴더명이 됨
        attrlist.append(attr)

    return attrlist


#test code
# 먼저 실행되어야 함. working 디렉토리 변경
os.chdir(BASE_PATH)
cate_main()