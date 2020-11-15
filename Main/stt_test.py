# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START speech_transcribe_streaming_mic]
from __future__ import division

import re
import sys
import os

from google.cloud import speech

import pyaudio
from six.moves import queue
from weather import WeatherModule
from tts import TTS
from classification import Classification


# Audio recording parameters
RATE = 44100#16000
CHUNK = 4096#int(RATE/10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
            input_device_index = 1
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

'''Clova 음성 파일 재생하는 함수'''
import pygame
def play(audio_name):
    pygame.mixer.init()
    pygame.mixer.music.load('../data/' + audio_name)
    pygame.mixer.music.play()
    # 필요해
    while pygame.mixer.music.get_busy() == True:
        continue


flag = 0
weather = WeatherModule()
tts = TTS()
classification = Classification()

# 리턴 0 추가 --> 스피커에서 소리가 나오면 리턴을 하게되고 해당 리턴값으로 다시 tts를 출력.
def compare(transcript):

    # 함수안에서 전역변수 수정하기 - global
    global flag

    # 모든 공백 제거
    text = transcript.strip()
    text = text.replace(" ", "")

    if (flag == 0 and '안녕' in text):
        # 전역변수인 flag를 안녕을 함으로써 1로 바꿔줌. 1이 계속 유지되있는상태. 언제 0으로 다시 바꿀것인가..? --> 아래에 추가해놓은부분 주석처리 해놓긴했는데 실제로 테스트해봐야함.
        flag = 1
        print('===안녕')
        play("hello.mp3")  # 어떤 옷을 입으시겠어요?
        return False

    elif (flag == 1 and '날씨어때' in text):
        print('===날씨 ')
        w_list = weather.request_weather()
        # 날씨 + 기온 정보
        tts.synthesize_text(w_list[0])
        # 추천 옷차림 정보
        play(w_list[1])
        # 추가 멘트: 비 올때, 눈 올때
        if len(w_list) == 3:
            play(w_list[2])
        return True

    elif (flag == 1 and '옷알려줘' in text):
        print("===옷 ")
        # play("wait.mp3")
        color, pattern, shape = classification.execute()
        tts.synthesize_text("{} {} {} 입니다.".format(color, pattern, shape))
        return True

    # 고마워 말고 뭐 없나?
    elif (flag == 1 and '고마워' in text):
        flag = 0
        return False  ## 종료

    '''
    elif (flag == 1):
        play("pardon.mp3")
        print("pardon")
        # tts.synthesize_text("다시한번 말씀해주시겠어요?")
        return False
    '''
    return False


# api로부터 받은 응답을 받아서 화면에 출력하는 함수
def listen_print_loop(responses):

    global flag
    """
    반환형식 :
    {
  "results": [
    {
      "alternatives": [
        {
          "confidence": 0.98267895,
          "transcript": "how old is the Brooklyn Bridge"
          }
        ]

    각 응답은 여러개의 results와 여러개의 대체택스트로 이루어져있는데 여기서는
    가장 최상위 result의 최상의 alternative의 transcript만 가져옴

    전달된 음성이 중간지점이였을경우 말 한마디(?)가 끝날때까지 계속해서 출력되는듯 --> 그렇게 안되도록 수정했음!
    """
    num_chars_printed = 0

    # 스트리밍으로 받아오는 응답에 대해
    for response in responses:
        # 제공된 오디오에서 음성을 인식할 수 없는경우 반환된 results목록에 항목이 없게됨.
        if not response.results:
            continue

        # 응답중 가장 최상위 results를 사용하겠다.
        result = response.results[0]

        # 0번째 result에 응답이 없으면 다시반복 .
        if not result.alternatives:
            continue

        # 인식된 텍스트값
        transcript = result.alternatives[0].transcript

        # overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        # END_OF_SINGLE_UTTERANCE 이벤트 발생시 stt result text를 반환.
        # 말의 끝맺음으로써 스트리밍 인식을 종료하도록함. ( 안녕 -->이 말의 끝맺음으로 구글서버가 인식을 못하면 소용이 없긴함...)
        '''
        if response.speech_event_type:
            #이게 출력된다면 우리가 말한말을 끝맺음이라 판단하고 뒤에나오는 말들은 인식 안함 --> 오디오파일 재생후에 다시 STT호출하는 코드를 추가함

            print('final text: ', transcript)
            return transcript
        '''
        """말의 끝맺음이 아니면 --> 막 계속 말하면 is_final이 result에 포함이 안되고 말이 끝낫을때 돌아오는 응답에만 is_final이 포함되서 돌아옴!!! 
        ex) 우리 그래서 뭐먹어 --> 우리, 우리 그래서, 우리 그래서 뭐, 이런식으로 is_final값이 없이 응답이 계속해서 오다가 '우리그래서 뭐먹어' 가 한번에 모두 반환되는 시점의 응답에서 is_final = true가 추가되서 옴! 
        근데 밑에서 파라미터 interim_results = false로 추가해서 이제 중간단계들은 리턴안하고 말 한덩이가 끝날때만 응답이 오도록 바꿈."""
        # if not result.is_final:
        # num_chars_printed = len(transcript)

        # 응답이 있고, 말도 끝났다면? --> 우리가 주로 쓰게될부분!!! (is_final = true)
        if result.is_final:
            # (이게 출력되는 중이라면 우리가 말한말이 끝맺음이라고 판단하지 않고 stt계속 대기하는상태
            print('me (is_final): ', transcript)
            compare(transcript)
            # 한마디 말하고 그에대한 응답이 compare에서 실행되면 다시 포문으로 돌아가서 다음 말한마디에 대한 compare함수 실행

            #num_chars_printed = 0


def main():

    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ko-KR'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        #  single_utterance=True 파라미터 추가함 --> single spoken utterance만 인지해서 응답해줌
        # 중간에 말을 멈추거나 하면 스트리밍인식을 종료함 --> 스피커소리 다시 인식 안하게됨
        #single_utterance=True,
        # false로 바꿧어. 이렇게 바꾸면 is_final 이 true인것만 반환함
        interim_results=True)


    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # listen_print_loop가 리턴해도 다시 실핼될 수 있도
        listen_print_loop(responses)
        print('main: finished listen_print_loop')



if __name__ == '__main__':
    play('start.mp3')
    main()
# [END speech_transcribe_streaming_mic]

