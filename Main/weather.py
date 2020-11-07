import requests

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

        info = [
            self.city_name,
            data_weather[0]['main'],
            data_weather[0]['description'],
            round(data_main['temp'], 2),
            round(data_main['temp_min'], 2),
            round(data_main['temp_max'], 2),
        ]
        # info: list[도시 이름, 날씨(영어), 날씨 설명(한국어), 현재기온, 최저기온, 최고기온]

        weather = "오늘 날씨는 "+ data_weather[0]['description'] +\
                 ". 현재 기온은 " + str(round(data_main['temp'], 2)) +'도'+\
                 '. 최저 기온은 '+str(round(data_main['temp_min'], 2))+'도'+\
                 '. 최고 기온은 '+str(round(data_main['temp_max'], 2))+'도 입니다.'


        temp_mid = int(round(data_main['temp_max'], 2)) - int(round(data_main['temp_min'], 2))



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


        recommend_start = '오늘 날씨에는'
        clothe = ''
        recommend_end = '을 추천합니다.'

        ㄴif temp_mid >=28:
          clothe = recommend_start + clotheslist[0] + recommend_end
          
        elif temp_mid>= 27 and temp_mid<=23:
          clothe = recommend_start + clotheslist[1] + recommend_end

        elif temp_mid>=20 and temp_mid<=22:
          clothe = recommend_start + clotheslist[2] + recommend_end
        
        elif temp_mid>= 17 and temp_mid<=19:
          clothe = recommend_start + clotheslist[3] + recommend_end
        
        elif temp_mid>= 12 and temp_mid<=16:
          clothe = recommend_start + clotheslist[4] + recommend_end
        
        elif temp_mid>= 9 and temp_mid<=11:
          clothe = recommend_start + clotheslist[5] + recommend_end
        
        elif temp_mid>= 5 and temp_mid<=8:
          clothe = recommend_start + clotheslist[6] + recommend_end
        
        else:
          clothe = recommend_start + clotheslist[7] + recommend_end




        return weather, clothe



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
