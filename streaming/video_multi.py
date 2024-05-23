from time import sleep
from datetime import datetime
import cv2
from base_camera import BaseCamera
import requests
import pickle

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


    #def get_frames():   
    #     all_data=requests.get('http://127.0.0.1:8000/api/live')
    #     #all_data=requests.get('http://192.168.11.38:8001/api/live')
    #     frame_data=(pickle.loads(all_data))#元の形式にpickle.loadsで復元
    #     result="ok"
    #     return result,frame_data
