
# 나중에 신경망코드에 쓸때 클래스가 무조건 편하니까 클래스로 만들엇오
# 글구 보고서쓸때도 클래스별로 쓰면 좋을거같아서뤼 근데나도 파이썬 클래스몇번 안만들어봐서 self가 먼지 구글링해봄 ㅋㅋ
class DataProcessing:

    # 매개변수 - index :찾고자하는 속성값 인덱스 / list : 이미지속성값 배열
    def findImage(self,index, list):
        # 찾고자하는 인덱스값이 배열의 1의 인덱스값과 같으면 그 이미지는 해당속성을 갖고있는것!
        if index == list.index('1'):
            print("이 이미지는", index, "번째 속성을 가진 이미지임_폴더로 뺴내는 코드 여기에 작성")
            # 폴더로 빼내는 코드작성 --> 하영
        else:
            print("해당속성값을 가지지 않는 이미지입니다. ")

    # txt파일읽어서 이름,숫자로 나눠서 숫자는 리스트(배열)로 변환하고 묶어서 딕셔너리변수에 저장하는 함수
    def makeList(self):
        filepath = '/Users/iseungjin/2020_3_2/capstone/list_attr_img.txt'
        # 읽기모드로 파일오픈 (r - 읽기모드)
        f = open(filepath, 'r')
        # 나중에는 100대신 line 총 개수 넣으면 됨
        for i in range(100):
            line = f.readline()
            line = line.replace("                        ", ",")
            # , 있는부분을 찾아서 처음부터 거기까지는 옷이미지 저장경로 그뒤로는 이미지에대한 속성값
            image_name = line[:line.find(',')]
            image_val = line[line.find(',') + 1:]
            # 문자열 배열로 변환
            image_val_list = image_val.split()
            # 이미지속성값에 1이 없으면 오류남 - 1없으면 다시 위로올라가서 다음줄읽고 1이 있을때만 밑에코드 실행
            if '1' not in image_val_list:
                continue
            else:
                self.findImage(717, image_val_list)
                # 튜플 형식의 dataset에 저장!
                dataset = {image_name: image_val_list}
                print(dataset)
                

dataprocessing = DataProcessing()
dataprocessing.makeList()

# 특정 속성값을 갖는 이미지인지 아닌지 확인하는 함수 호출!

# 한 덩어리당 24줄이니까 포문써서 24줄을 한단위로 읽어들인다음에 이미지이름 / 숫자배열로 나눠서 저장
# 숫자배열중에서 34번째 인덱스가 1인 이미지들만 뽑아서 저장 --> if ( 34 == list.index('1')) 이면 이미지저장
# ( 예를들어 34번재 인덱스가 꽃무늬 패턴이다? - 해당 이미지를 꽃무늬패턴폴더에 저장)
# 근데 717 뒤에 또다른 속성값 가지고 있을때 다시 범위지정 해줘야함.. 뒤에부분부터 찾으면 800얼마에 또 1 잇긴함
