# 실행 전 path와 driver만 경로 설정 해주면 됨! (맨 밑부분에 있음)
# 검색어 바꿔가면서 실행하면 됨

import time
import socket
import os
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException


def scroll_down():
    scroll_count = 0

    print("ㅡ 스크롤 다운 시작 ㅡ")

    # 스크롤 위치값 얻고 last_height 에 저장
    last_height = driver.execute_script("return document.body.scrollHeight")
    last_height = str(last_height)
    # 더보기 버튼 클릭한 횟수
    after_click = 0

    # 최대 3번만 더보기 버튼 클릭하기 (더보기 1번만 눌러도 약 650장 정도 나옴)
    while after_click < 3:
        # 스크롤 다운
        driver.execute_script("window.scrollTo("+last_height+", document.body.scrollHeight);")
        scroll_count += 1
        # 스크롤 새로 생길 때까지 잠시 기다림
        time.sleep(1)

        # 스크롤 위치값 얻고 new_height 에 저장
        new_height = driver.execute_script("return document.body.scrollHeight")
        new_height = str(new_height)

        # 스크롤이 최하단일 때
        if last_height == new_height:
            print("ㅡ 스크롤 횟수:", scroll_count)
            # 더보기 버튼 나올때까지 잠시 기다림
            time.sleep(1.5)
            # 더보기 버튼이 있으면 클릭
            if driver.find_element_by_xpath(f'//*[@id="islmp"]/div/div/div/div/div[5]/input').is_displayed():
                driver.find_element_by_xpath(f'//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
                after_click += 1
                print(f"ㅡ 더보기 횟수: {after_click} ㅡ")
            # 없으면 종
            elif NoSuchElementException:
                print("ㅡ NoSuchElementException ㅡ")
                print("ㅡ scroll_down() return ㅡ")
                break

        last_height = str(new_height)


def click_and_retrieve(index, img, img_list_length):
    global crawled_count
    try:
        img.click()
        driver.implicitly_wait(3)

        # html에서 이미지 소스가 들어있는 코드 부분
        src = driver.find_element_by_xpath(
            '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute('src')

        # <이미지 저장할 폴더의 경로>/crawling/<크롤링한 횟수>_<검색어>.jpg로 이미지 저장
        # ex) /Users/hayeong/Smart-Closet_local/database/crawling/무지티/1_무지티.jpg
        if src.split('.')[-1] == "png":
            urlretrieve(src, path + '/' + str(crawled_count + 1) + '_' + query + ".png")
            print(f"{index + 1} / {img_list_length} (png)")
        else:
            urlretrieve(src, path + '/' + str(crawled_count + 1) + '_' + query + ".jpg")
            print(f"{index + 1} / {img_list_length} (jpg)")
        crawled_count += 1

    except HTTPError:
        print("ㅡ HTTPError & 패스 ㅡ")
        pass


def crawling(query):
    global crawled_count

    print("ㅡ 크롤링 시작 ㅡ")

    # 이미지 고급검색 중 이미지 유형 '사진'
    url = f"https://www.google.com/search?as_st=y&tbm=isch&hl=ko&as_q={query}&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:photo"
    driver.get(url)
    driver.maximize_window()
    scroll_down()

    div = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]')
    # class_name에 공백이 있는 경우 여러 클래스가 있는 것이므로 아래와 같이 css_selector로 찾음
    img_list = div.find_elements_by_css_selector(".rg_i.Q4LuWd")

    # img_list: 현재 윈도우에 보이는 이미지들의 리스트
    for index, img in enumerate(img_list):
        try:
            click_and_retrieve(index, img, len(img_list))

        except ElementClickInterceptedException:
            print("ㅡ ElementClickInterceptedException ㅡ")
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
            time.sleep(3)
            click_and_retrieve(index, img, len(img_list))

        except NoSuchElementException:
            print("ㅡ NoSuchElementException ㅡ")
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
            time.sleep(3)
            click_and_retrieve(index, img, len(img_list))

        except ConnectionResetError:
            print("ㅡ ConnectionResetError & 패스 ㅡ")
            pass

        except URLError:
            print("ㅡ URLError & 패스 ㅡ")
            pass

        except socket.timeout:
            print("ㅡ socket.timeout & 패스 ㅡ")
            pass

        except socket.gaierror:
            print("ㅡ socket.gaierror & 패스 ㅡ")
            pass

        except ElementNotInteractableException:
            print("ㅡ ElementNotInteractableException ㅡ")
            break

    try:
        print("ㅡ 크롤링 종료 (성공률: %.2f%%) ㅡ" % (crawled_count / len(img_list) * 100.0))

    except ZeroDivisionError:
        print("ㅡ img_list 가 비어있음 ㅡ")

    driver.quit()


# clickAndRetrieve() 과정에서 urlretrieve 이 너무 오래 걸릴 경우를 대비해 타임 아웃 지정
socket.setdefaulttimeout(30)

# 이미지들이 저장될 경로 및 폴더 이름
path = "/Users/iseungjin/2020_3_2/capstone/crawling_img"

# 드라이버 경로 지정 (크롬 이용) -> 컴퓨터에 chromedriver 설치해야 함 (구글에 치면 다운 가능)
driver = webdriver.Chrome('/Users/iseungjin/chromedriver')

# 크롤링한 이미지 수
crawled_count = 0
# 검색어 입력 받기
query = input("입력: ")
# 검색어로 새폴더 만들기
path = path+'/'+query
os.makedirs(path)
crawling(query)