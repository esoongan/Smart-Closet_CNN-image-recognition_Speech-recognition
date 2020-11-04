import numpy as np
import cv2
from sklearn.cluster import KMeans
from Color.lab_converter import ColorConverter            # RGBconverter -> ColorConverter
import matplotlib.pyplot as plt
import time

# NOTE #
# 옷 색깔의 평균을 구하려면 bbox로 꼭 배경을 잘라낸 사진이어야함

# rgb를 색상명으로 맵핑하는 클래스, 매개변수로 색상명 정보를 가진 txt파일 경로
converter = ColorConverter()
# 이미지 로드
image = cv2.imread(
    "/Users/hayeong/Desktop/Capstone/DeepFashion DB/pattern_dir/dots/img_00007795.jpg")  # test image

# 배경색 제거를 위한 이미지 자르기
h, w, _ = image.shape
image = image.copy()
image = image[int(h*0.2) : int(h*0.8), int(w*0.2) : int(w*0.8)] # [시작 height : 끝 height, 시작 width : 끝 width]

# 자른 이미지 보기
cv2.imshow('image', image)
##### 사진 보고 아무 키나 쳐야 결과가 출력됨 #####
cv2.waitKey(0)

print(time.time())
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# height와 width를 통합하여 하나의 array로 만듬
image = image.reshape((image.shape[0] * image.shape[1], 3))

##### k-mean 알고리즘(비지도 학습에서 가장 보편적인 알고리즘)으로 이미지 학습 ######
# k개의 데이터 평균을 만들어 데이터를 클러스팅하는 알고리즘
k = 5 # 추출할 클러스터 개수
# k-mean 알고리즘을 이용한 비지도 학습 실행
clt = KMeans(n_clusters=k).fit(image)
# 생성한 k개의 cluster 각각의 중심값이 담긴 리스트
centers = clt.cluster_centers_

# 클러스터로 추출한 컬러가 (k개의 클러스터 중) 차지하는 비율을 반환
def get_weights(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    histogram = hist.astype("float")
    histogram /= hist.sum()

    # return the histogram
    return histogram


# 각 클러스터의 가중치로 사용할 것임
# W의 모든 값을 더하면 1임
W = get_weights(clt)
print(W)
# W를 내림차순으로 정렬하기 위해 {index:W} 딕셔너리를 만듬
w_dict = {}
for w in range(k):
    w_dict[w] = W[w]

# 내림차순 정렬
w_dict = sorted(w_dict.items(), reverse=True, key=lambda item: item[1])

# 평균값 구하는 방법
# 1. 클러스터 전체의 평균값 구하기
# 2. 가장 지배적인 클러스터의 색상 하나만 출력  ex)검정 55% 흰색 30% 파랑 10% => 검정색 출력
# 3. 특정 % 이상 차지하는 것들로만 평균값 구하기
# 4. 각각의 %가 비슷하게 나왔으면 각 색상을 모두 출력하기 ex)검정 30% 흰색 30% => 검정색, 흰색 모두 출력
# 5. 특정 % 이상 차지하는 것이 있으면 그 것 하나만 출력, 아니면 상위 2개의 색을 출력
'''
def get_average1():
    rgb = np.zeros(3)
    for i in range(k):
        wcenter = centers[i] * W[i]

        # rgb값이 0~255 사이의 정수값을 가짐
        rgb[0] += wcenter[0]
        rgb[1] += wcenter[1]
        rgb[2] += wcenter[2]

        # 소수점 밑 2자리까지 반올림
        rgb = rgb.round(2)
    return rgb


def get_average2():
    index = -1
    max_w = -1
    for i in range(k):
        if W[i] > max_w:
            max_w = W[i]
            index = i
    rgb = centers[index]
    return rgb


def get_average4():
    rgb = np.zeros((k, 3))
    count = 0
    for i in range(k):
        # 30프로 이상인 색상 모두 출
        if W[i] >= 0.3:
            rgb[count] = centers[i]
            count += 1
    return count, rgb
'''


# baseline% 이상 차지하는 색상이 있을 경우 -> 해당 색상 하나만 출력
# 그 외 -> 상위 2개의 색상 모두 출
# ([r,g,b], W) 튜플의 리스트를 리턴함
def get_dominent_rgb(baseline):
    # w_dict[0]은 가장 비율이 높은 색의 튜플, (해당 클러스터의 인덱스, 해당 클러스터의 비율)임
    clt_index, w = w_dict[0]

    rgb_tuple_list = [(centers[clt_index], w)]
    # 가장 큰 비율이 baseline 이상이면 하나의 색만 리턴
    if w >= baseline:
        # rgb_tuple_list에는 하나의 ([r,g,b], w) 튜플만 들어있음
        return rgb_tuple_list

    # baseline 이상인 것이 없으면 상위 2개의 색 리턴
    clt_index, w = w_dict[1]
    rgb_tuple_list.append((centers[clt_index], w))

    clt_index, w = w_dict[2]
    rgb_tuple_list.append((centers[clt_index], w))
    # rgb_tuple_list에는 두개의 ([r,g,b], w) 튜플이 들어있
    return rgb_tuple_list




# 색상의 평균값 출력
print('*** OUTPUT ***')
# 0.6(=baseline) 이상 차지하는 색상이 있으면 그 색상 하나만 리턴
rgb_tuple_list = get_dominent_rgb(0.6)


for i in range(len(rgb_tuple_list)):
    rgb = []
    rgb, w = rgb_tuple_list[i]

    # 이미지에서 가장 지배적인 순대로 rgb를 추출, 색상명과 맵핑
    color_name = converter.rgb_to_name(rgb)
    # 해당 색상명과 그 색상이 차지하는 비율을 함께 출력
    print('Color Name[', i,']=', color_name, w, '%')
print(time.time())

# 추출한 k개의 클러스터의 중심 색상을 히스토그램 그래프로 출력함
# 클러스터 확인용 (추후 이용x)
def plot_colors(W, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(W, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX
    # return the bar chart
    return bar



bar = plot_colors(W, centers)

plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()