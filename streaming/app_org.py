import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

import requests
import pickle
import cv2
from time import sleep
from datetime import datetime
from base_camera import BaseCamera

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
   return templates.TemplateResponse('index.html', {"request": request})

def gen(camera): #Video streaming generator function
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():#Video streaming route. Put this in the src attribute of an img tag
    return  StreamingResponse(gen(Camera()),
                    media_type='multipart/x-mixed-replace; boundary=frame')

class Camera(BaseCamera):
    def __init__(self):
        super().__init__()
    # over-wride of BaseCamera class frames method
    @staticmethod
    def frames():
        while True:
            frame_data=b''  
            headers = {'Content-Type': 'application/octet-stream'}
            res=requests.get('http://127.0.0.1:8000/api/live')
            print(">>> ",res,datetime.now())
            all_data=res.content
            try:
                frame_data=(pickle.loads(all_data))#元の形式にpickle.loadsで復元
                yield cv2.imencode('.png', frame_data)[1].tobytes() #'.png'で背景透明も返すことができた。元は.JPG
            except:
                print("flame error")
            sleep(0.05)   #フレーム数が決まる

            

if __name__ == "__main__":
    print('stop: ctrl+c')
    uvicorn.run(app, host="0.0.0.0", port=5000)

