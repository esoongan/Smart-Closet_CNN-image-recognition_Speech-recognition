import cv2

import matplotlib.pyplot as plt

import matplotlib.image as mpimg


#1,RGB이미지를 HSV이미지로 변환
#--> 이미지는 하영이가 만든 코드에서 마지막에 색상 bar로 나타난 부분 bar를 이미지로 입력받는다(여러 색깔이 있다)

#2,색상 범위에 따라 특정 색상 객체을 추출하는 mask를 만듬
# -->색상범위 지정. 지금은 주황,초록, 파랑만 있음 추가 예정

#3,mask에 따라 이미지를 계산하여 특정한 색상의 객체만 추출
# 이 추출한 이미지를 다시 이미지 인식 코드의 인풋으로 넣는다


#이미지의 경로
imgpath = 'C:/colortest.jpg'

# 색상 범위 설정 --> opencv에서 색조 범위는 0~180이므로 HSV색상표 값에서 1/2 해야한다.
#색조, 채도, 명도
# 범위를 정하여 hsv이미지에서 원하는 색 영역을 바이너리 이미지로 생성한다.
#일단은 이 부분은 주황, 초록, 파랑 뿐 이지만 다른 색들도 찾아서 추가할 예정


lower_orange = (100, 200, 200)
upper_orange = (140, 255, 255)


lower_green = (30, 80, 80)
upper_green = (70, 255, 255)


lower_blue = (0, 180, 55)
upper_blue = (20, 255, 200)



# 이미지 파일을 읽어온다

img = mpimg.imread(imgpath, cv2.IMREAD_COLOR)

# BGR to HSV 변환 --> hue가 일정 범위를 가지는 순수한 색 정보를 가지기 떄문에 쉽게 색 분류 가능

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 색상 범위를 제한하여 mask 생성-->
# HSV이미지 픽셀값과 내가 원하는 색상 범위를 비교해서 픽셀 값이 색상 범위 안에 있을 경우, 그에 대응되는 위치의 마스크 행렬의 원소값에 1 입력

img_mask = cv2.inRange(img_hsv, lower_green, upper_green)# 초록을 추출한다.


# 원본 이미지를 가지고 Object 추출 이미지로 생성

img_result = cv2.bitwise_and(img, img, mask=img_mask)

# 결과 이미지 생성
# 결과 이미지를(단 하나의 색) 하영이가 짠 코드의 input으로 넣어 색을 판별 할 수 있도록 하자.

imgplot = plt.imshow(img_result)

plt.show()
