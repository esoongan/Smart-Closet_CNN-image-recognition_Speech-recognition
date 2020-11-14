# export GOOGLE_APPLICATION_CREDENTIALS="Smart-Classification-28139a960cdf.json의 경로"
# cat ~/.bash_profile

# 구글 SDK 설치
# https://cloud.google.com/sdk/docs/quickstart?hl=ko#mac

# sudo pip install google-cloud-speech
# sudo pip install --upgrade google-api-python-client
# !pip install --upgrade google-cloud-texttospeech

# https://cloud.google.com/text-to-speech/docs/create-audio?hl=ko#text-to-speech-text-python
from google.cloud import texttospeech


class TTS:
    def __init__(self, abs_save_path='../data'):
        self.SAVE_PATH = abs_save_path

        self.client = texttospeech.TextToSpeechClient()

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Wavenet-A",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            # 오디오 볼륨: [-96.0, 16.0] (default = 0)
            # volumeGainDb=6
        )

    def set_path(self, abs_path):
        self.SAVE_PATH = abs_path

    def synthesize_text(self, text):
        """Synthesizes speech from the input string of text."""
        # [api key].json 파일이 있는 경로
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =\
        #    "/home/pi/smartcloset/Smart-Classification-28139a960cdf.json"
        input_text = texttospeech.SynthesisInput(text=text)

        response = self.client.synthesize_speech(
            request={"input": input_text, "voice": self.voice, "audio_config": self.audio_config}
        )

        with open(self.SAVE_PATH+'/output.mp3', "wb") as out:
            out.write(response.audio_content)
        print('[' + text + '] written to file "' + self.SAVE_PATH + '"/output.mp3"')

        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(self.SAVE_PATH + '/output.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

