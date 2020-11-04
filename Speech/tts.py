# export GOOGLE_APPLICATION_CREDENTIALS="Smart-Closet-28139a960cdf.json의 경로"
# cat ~/.bash_profile

# 구글 SDK 설치
# https://cloud.google.com/sdk/docs/quickstart?hl=ko#mac

#sudo pip install google-cloud-speech
#sudo pip install --upgrade google-api-python-client
#!pip install --upgrade google-cloud-texttospeech

# https://cloud.google.com/text-to-speech/docs/create-audio?hl=ko#text-to-speech-text-python
def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    import os

    # [api key].json 파일이 있는 경로
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/hayeong/Smart-Closet/SClocal/Smart-Closet-28139a960cdf.json"

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("../SClocal/output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")


synthesize_text("안녕 이 옷은 빨간 색이야")