from pathlib import Path
import voicevox_core
from voicevox_core import AccelerationMode, AudioQuery, VoicevoxCore

import uvicorn
from fastapi import FastAPI, Request, Form, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse,FileResponse
from starlette.responses import Response

app = FastAPI()

SPEAKER_ID = 2

open_jtalk_dict_dir = './open_jtalk_dic_utf_8-1.11'
text = 'こんにちはめぐです。'
acceleration_mode = AccelerationMode.AUTO

core = VoicevoxCore(
        acceleration_mode=acceleration_mode,
        open_jtalk_dict_dir=open_jtalk_dict_dir
        )
core.load_model(SPEAKER_ID)

@app.post('/api/vox_tts')
def vox_tts(text: str = Form(...),speaker_id: int = Form(SPEAKER_ID), pitch: float = Form(0), speed: float = Form(0), intonation: float = Form(0)):
    
    audio_query = core.audio_query(text, speaker_id)
    audio_query.pitch_scale += pitch
    audio_query.speed_scale += speed
    audio_query.intonation_scale += intonation
    
    wav = core.synthesis(audio_query, speaker_id)

    return Response(content=wav, media_type="audio/wav")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8013)
