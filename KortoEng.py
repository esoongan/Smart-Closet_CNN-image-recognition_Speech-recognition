import glob
import shutil

# 한글이름으로된 옷사진 들만 저장된 폴더
kor_path = "/Users/iseungjin/2020_3_2/capstone/inputdata/무지"
# 옮겨질 폴더
dest_path = '/Users/iseungjin/2020_3_2/capstone/inputdata/pattern/None_4'

files = glob.glob(kor_path+'/*.jpg')

for i, f in enumerate(files):
    print(f)
    eng_name = '/none_crawling%d.jpg'%i
    #f = f.replace(f[start_point+1:], eng_name)
    # 파일 이름을 위의 eng_name으로 변경하고 해당패턴 폴더로 이동시키기
    shutil.move(f, dest_path+eng_name)