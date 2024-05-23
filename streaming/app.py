import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import requests
import pickle
import cv2
from time import sleep
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

def generate_frames():
    while True:
        start_time=time.time()
        response = requests.get('http://127.0.0.1:8000/api/live')  # 外部APIからのレスポンス
        all_data = response.content  # レスポンスのコンテンツ（バイナリデータ）

        # pickleを使用してバイナリデータから画像データを復元
        try:
            frame_data = pickle.loads(all_data)  # 画像データのデシリアライズ
            _, buffer = cv2.imencode('.png', frame_data)  # JPEG形式にエンコード
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Frame error: {e}")

        sleep(0.02)  # フレームレートの制御
        print("Definec frame time=",'{:.2f}'.format((time.time()-start_time)*1000),"mS")

@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    return StreamingResponse(generate_frames(),
                             media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print('Server is running. Stop: ctrl+c')
    uvicorn.run(app, host="0.0.0.0", port=5000)
