# from weather.py import WeatherAPI

# weatherAPI = WeatherAPI()
# weather = weatherAPI.request_weather()
# 날씨 정보 리스트 게또


import requests


class WeatherAPI:
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
        self.city_id = self.city_list[0]['city_id']
        self.city_name = self.city_list[0]['city_name']
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
        return info

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