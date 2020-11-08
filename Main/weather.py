import requests
import numpy as np


class WeatherModule:
    city_list = [
        {'name': 'Seoul', 'city_id': '1835847'},
        {'name': 'Busan', 'city_id': '1838524'},
        {'name': 'Daegu', 'city_id': '1835329'},
        {'name': 'Incheon', 'city_id': '1843564'},
        {'name': 'Gwangju', 'city_id': '1841811'},
        {'name': 'Daejeon', 'city_id': '1835235'},
        {'name': 'Ulsan', 'city_id': '1833747'},
        {'name': 'Sejong', 'city_id': '1835235'},
        {'name': 'Gyeonggi', 'city_id': '1841610'},
        {'name': 'Gangwon', 'city_id': '1843125'},
        {'name': 'Chungcheongbuk', 'city_id': '1845106'},
        {'name': 'Chungcheongnam', 'city_id': '1845105'},
        {'name': 'Jeollabuk', 'city_id': '1845789'},
        {'name': 'Jeollanam', 'city_id': '1845788'},
        {'name': 'Gyeongsangbuk', 'city_id': '1841597'},
        {'name': 'Gyeongsangnam  ', 'city_id': '1902028'},
        {'name': 'Jeju', 'city_id': '1846266'},
    ]
    url = 'http://api.openweathermap.org/data/2.5/weather'

    w_ko = np.array(["가벼운 비를 동반한 천둥구름", "비를 동반한 천둥구름", "폭우를 동반한 천둥구름", "약한 천둥구름",
                     "천둥구름", "강한 천둥구름", "불규칙적 천둥구름", "약한 연기와 안개를 동반한 천둥구름", "연기와 안개를 동반한 천둥구름",
                     "강한 안개비를 동반한 천둥구름", "가벼운 안개비", "안개비", "강한 안개비", "가벼운 적은비", "적은비",
                     "강한 적은비", "소나기와 안개비", "강한 소나기와 안개비", "소나기", "약한 비", "중간 비", "강한 비",
                     "매우 강한 비", "엄청난 폭우", "우박", "약한 소나기 비", "소나기 비", "강한 소나기 비", "불규칙적인 소나기 비",
                     "가벼운 눈", "눈", "강한 눈", "진눈깨비", "소나기 진눈깨비", "약한 음비와 눈", "비와 눈", "약한 소나기 눈",
                     "소나기 눈", "강한 소나기 눈", "엷게 낀 안개", "연기", "연기와 안개", "모래 먼지", "안개", "모래", "먼지", "화산재", "돌풍",
                     "토네이도", "구름 한 점 없는 맑은 하늘", "약간의 구름이 낀 하늘", "드문드문 구름이 낀 하늘", "구름이 거의 없는 하늘",
                     "구름으로 뒤덮인 흐린 하늘", "토네이도", "태풍", "허리케인", "추움", "더움", "바람", "우박", "바람이 거의 없음",
                     "약한 바람", "부드러운 바람", "중간 세기 바람", "신선한 바람", "센 바람", "돌풍에 가까운 센 바람", "돌풍",
                     "심각한 돌풍", "폭풍", "강한 폭풍", "허리케인"])

    w_id = np.array([200, 201, 202, 210, 211, 212, 221, 230, 231, 232,
                     300, 301, 302, 310, 311, 312, 313, 314, 321, 500,
                     501, 502, 503, 504, 511, 520, 521, 522, 531, 600,
                     601, 602, 611, 612, 615, 616, 620, 621, 622, 701,
                     711, 721, 731, 741, 751, 761, 762, 771, 781, 800,
                     801, 802, 803, 804, 900, 901, 902, 903, 904, 905,
                     906, 951, 952, 953, 954, 955, 956, 957, 958, 959,
                     960, 961, 962])

    def __init__(self):
        # 지역은 울로 고정
        self.city_id = self.city_list[0]['city_id']
        self.city_name = self.city_list[0]['name']
        self.params = dict(
            id=self.city_id,
            APPID='cca4a0e8a29e94fe7104d38628c9401a',
            lang='kr',
            units='metric'
        )

    def request_weather(self):
        resp = requests.get(url=self.url, params=self.params)
        data = resp.json()
        if (data['cod'] == 429):  # blocking error code
            print('error code = 429')

        data_weather = data['weather']
        data_main = data['main']
        id = data_weather[0]['id']

        '''
        info = [
            self.city_name,
            data_weather[0]['main'],
            data_weather[0]['description'],
            round(data_main['temp'], 2),
            round(data_main['temp_min'], 2),
            round(data_main['temp_max'], 2),
        ]
        # info: list[도시 이름, 날씨(영어), 날씨 설명(한국어), 현재기온, 최저기온, 최고기온]
        '''

        i = np.where(self.w_id == id)[0][0]
        description = self.w_ko[i]

        weather = "오늘 날씨는 " + description + \
                  "입니다. 현재 기온은 " + str(round(data_main['temp'], 2)) + '도' + \
                  '. 최저 기온은 ' + str(round(data_main['temp_min'], 2)) + '도' + \
                  '. 최고 기온은 ' + str(round(data_main['temp_max'], 2)) + '도 입니다.'

        temp_mid = (int(round(data_main['temp_max'], 2)) + int(round(data_main['temp_min'], 2))) / 2

        '''
                clotheslist = ['민소매, 반팔, 반바지, 치마',
                '반팔, 얇은 셔츠, 반바지, 면바지',
                '얇은가지건, 긴팔티, 면바지, 청바지',
                '얇은니트, 가디거, 맨투맨, 얇은자켓, 면바지, 청바지',
                '자켓, 가디건, 야상, 맨투맨, 니트, 스타킹, 청바지, 면바지',
                '코트, 히트텍, 니트, 청바지, 레깅스',
                '패딩, 두꺼운 코트, 목도리, 기모제품']
         내 기억에 tts가 _를 밑줄로 했던 것 같아서 첨에 이거로 하다가 ,를 컴마라고 말할까 두렵소,,
        '''

        clotheslist = ['민소매 반팔 반바지 그리고 치마',
                       '반팔 얇은셔츠 반바지 그리고 면바지',
                       '얇은가지건 긴팔티 면바지 그리고 청바지',
                       '얇은니트 가디거 맨투맨 얇은자켓, 면바지, 청바지',
                       '자켓 가디건 야상 맨투맨 니트 스타킹 청바지 그리고 면바지',
                       '코트 히트텍 니트 청바지 그리고 레깅스',
                       '패딩 두꺼운코트 목도리 그리고 기모제품']

        ret = [weather]

        if temp_mid >= 28:
            ret.append('01_recommend.mp3')  # 01_오늘은_매우_더우니_민소매_반팔에_반바지_치마를_추천드려요
        elif temp_mid >= 27 and temp_mid <= 23:
            ret.append('02_recommend.mp3')  # 02_오늘은_조금_더우니_반팔_또는_얇은_셔츠에_반바지나_면바지를_추천드려요
        elif temp_mid >= 20 and temp_mid <= 22:
            ret.append('03_recommend.mp3')  # 03_오늘은_따뜻하니_얇은_가디건_또는_긴팔티에_면바지나_청바지를_추천드려요
        elif temp_mid >= 17 and temp_mid <= 19:
            ret.append('03_recommend.mp3')
        elif temp_mid >= 12 and temp_mid <= 16:
            ret.append('04_recommend.mp3')  # 04_오늘은_선선하니_얇은니트_가디건_맨투맨_얇은자켓에_면바지나_청바지를_추천드려요
        elif temp_mid >= 9 and temp_mid <= 11:
            ret.append('05_recommend.mp3')  # 05_오늘은_쌀쌀하니_자켓_가디건_야상_니트에_청바지_또는_면바지를_추천드려요
        elif temp_mid >= 5 and temp_mid <= 8:
            ret.append('06_recommend.mp3')  # 06_오늘은_추우니_코트_히트텍_니트에_청바지_또는_레깅스를_추천드려요
        else:
            ret.append('07_recommend.mp3')  # 07_오늘은_엄청_추워요_패딩이나_두꺼운코트에_목도리와_기모제품을_추천드려요_꽁꽁_싸매고_

        # 추가 멘트
        # 비
        if int(id/100) == 5:
            ret.append('rain.mp3')  # 나가실+때+우산+챙기세요
        # 눈
        elif int(id/100) ==6:
            ret.append('snow.mp3')  # 눈에+미끄러지지+않게+조심해야겠어요

        # 리스트로 리턴
        # tts(ret[0]), play(ret[1]), if(len(ret)==3): play(ret[2])
        return ret


# data format
'''
{
  "coord": {
    "lon": -122.08,
    "lat": 37.39
  },
  "weather": [
    {
      "id": 800,                               *
      "main": "Clear",                         *
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 282.55,                             *
    "feels_like": 281.86,
    "temp_min": 280.37,                         *
    "temp_max": 284.26,                         *
    "pressure": 1023,
    "humidity": 100
  },
  "visibility": 16093,
  "wind": {
    "speed": 1.5,
    "deg": 350
  },
  "clouds": {
    "all": 1
  },
  "dt": 1560350645,
  "sys": {
    "type": 1,
    "id": 5122,
    "message": 0.0139,
    "country": "US",
    "sunrise": 1560343627,
    "sunset": 1560396563
  },
  "timezone": -25200,
  "id": 420006353,
  "name": "Mountain View",
  "cod": 200
  }                         
'''
