from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
import requests
from io import BytesIO
import time

def tts_voce(text,voice_id,pitch=0,speed=0,intonation=0):
    start_time=time.time()
    data= {"text":text,
           "speaker_id":voice_id,
           "pitch":pitch,
           "speed":speed,
           "intonation":intonation,}

    url="http://0.0.0.0:8013/api/vox_tts"
    response = requests.post(url,data=data) #リクエスト
    # ステータスコードが200（成功）の場合、ファイルに書き込む
    if response.status_code == 200:
        audio_data = BytesIO(response.content)
        wav = AudioSegment.from_file(audio_data, format="wav")
        print("voicebox gen time=",(time.time()-start_time)*1000,"mS")
        #play(wav)
    else:
        print(f"ファイルのダウンロードに失敗しました。ステータスコード: {response.status_code}")
        wav=""
    return response.status_code,wav
    #return response.status_code,audio_data

