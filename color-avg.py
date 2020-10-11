import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans
# NOTE #
# 옷 색깔의 평균을 구하려면 bbox로 꼭 배경을 잘라낸 사진이어야함
# 아래 코드는 이미지 전체에서 (배경 포함) 색상을 평균냄


# 이미지 로드
img = cv2.imread("/Users/hayeong/Smart-Closet_local/database/newimg/Tonal_Check-Patterned_Blouse/img_00000030.jpg")  # test image
# BGR순에서 RGB순으로 정렬
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# height와 width를 통합하여 하나의 array로 만듬
img = img.reshape((img.shape[0] * img.shape[1], 3))

##### k-mean 알고리즘(비지도 학습에서 가장 보편적인 알고리즘)으로 이미지 학습 ######
# k개의 데이터 평균을 만들어 데이터를 클러스팅하는 알고리즘
k = 5  # 추출할 클러스터 개수
# k-mean 알고리즘을 이용한 비지도 학습 실행
clt = KMeans(n_clusters=k).fit(img)
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


# 각 클러스터의 rgb값에 해당 클러스터의 비율 곱함
def get_average():
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


# 색상의 평균값 출력
new_rgb = get_average()
print('*** OUTPUT: Color Average [R,G,B]=', new_rgb, '***')

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
