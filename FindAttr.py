class DataProcessing:

    # 매개변수 - index :찾고자하는 속성값 인덱스 / list : 이미지속성값 배열
    def findImage(self, index, list):
        # 찾고자하는 인덱스값이 배열의 1의 인덱스값과 같으면 그 이미지는 해당속성을 갖고있는것!
        if index == list.index('1'):
            print("이 이미지는", index, "번째 속성을 가진 이미지임_폴더로 뺴내는 코드 여기에 작성")
            # 1 찾은부분부터 끝까지 중에서 1이또 있는지없는지 찾고 있으면 다시 if문 해서 해야댐 재귀호출하면될듯
            # 폴더로 빼내는 코드작성 --> 하영
        else:
            print("해당속성값을 가지지 않는 이미지입니다. ")

    # txt파일읽어서 이름,숫자로 나눠서 숫자는 리스트(배열)로 변환하고 묶어서 딕셔너리변수에 저장하는 함수
    def makeList(self):

        filepath = '/Users/iseungjin/2020_3_2/capstone/newfile.txt'
        # 읽기모드로 파일오픈 (r - 읽기모드)
        f = open(filepath, 'r')
        # 나중에는 100대신 line 총 개수 넣으면 됨
        for i in range(300):
            line = f.readline()
            line = line.replace("               ", ",")
            # , 있는부분을 찾아서 처음부터 거기까지는 옷이미지 저장경로 그뒤로는 이미지에대한 속성값
            image_name = line[:line.find(',')]
            image_val = line[line.find(',') + 1:]
            # 문자열 배열로 변환
            image_val_list = image_val.split()
            #이미지속성값에 1이 없으면 오류남 - 1없으면 다시 위로올라가서 다음줄읽고 1이 있을때만 밑에코드 실행
            if '1' not in image_val_list:
                continue
            else:
                self.findImage(39, image_val_list)
                # 튜플 형식의 dataset에 저장!
                dataset = {image_name: image_val_list}
                print(dataset)
        f.close()



dataprocessing = DataProcessing()
dataprocessing.makeList()
