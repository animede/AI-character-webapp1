import uvicorn
from fastapi import FastAPI, Form, UploadFile,File
from fastapi.responses import JSONResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

import shutil
from PIL import Image
import numpy as np
import cv2
import random, string
import io
import time
from time import sleep
import base64
import requests
import pickle
import threading

from face_d_api_class_s import AnimeFace_det

from voicebox_api import tts_voce
from pydub.playback import play
from socket import socket, AF_INET, SOCK_DGRAM
from del_bkg_api_class import DeleteBackground
from config import chr1_name,chr2_name,chr1_data,chr2_data

from l4 import Draw_l4

#---------------- global -----------------
global stream_image
global input_image
global pil_pose_image
global character_moving
global voice_message
global voice_new
global voice_thread
global audio_playng
global l3_scale
global l3_pos
global fps

app = FastAPI()

stb_url_local= 'http://0.0.0.0:8009/generate/'
rinct2_url = 'http://0.0.0.0:8012/generate'
elz_url = 'http://192.168.5.71:8012/generate/'
vhost = "127.0.0.1" # VOICEBOX サーバーIPアドレス定義 
vport = 3005        # VOICEBOXサーバー待ち受けポート番号定義
#Streamingのurl "0.0.0.0:5000"12
#frontのurl     "127.0.0.1:3000"

#クラス初期化
BG=DeleteBackground()
AF=AnimeFace_det()

fps=20
l3_scale=0.7    #デフォルト
l3_pos=[384,0]  #デフォルト

img_backgraund=Image.open("./背景/ピンク枠中.png")
bg_w,bg_h    = img_backgraund.size
l4_work = Image.new('RGBA', (bg_w, bg_h), (0, 0, 0, 0))

L4=Draw_l4("http://0.0.0.0",bg_w,bg_h)
pil_pose_image=Image.open("000001.png")
stream = np.array(img_backgraund, dtype=np.uint8)
stream_image = cv2.cvtColor(stream, cv2.COLOR_RGBA2BGRA)

character_moving="stop"
running_threads=False
voice_new = False
voice_thread = False
audio_playng =False

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのオリジンを設定
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
    )

@app.get("/api/live")
def live_video():
    global stream_image
    image = stream_image
    frame_data = pickle.dumps(image, 5)  # tx_dataはpklデータ
    return Response(content=frame_data, media_type="application/octet-stream")

#イメージのアップロード 背景とtkhはmodeは不要、llmmの時はマルチモーダルに渡すファイルです　face_detectでキャラ画像か背景かを自動判別
@app.post("/api/upload_file")
async def upload_file(file: UploadFile = File(...), mode:str = Form(...), user_name: str = Form(...)):
    global img_backgraund
    global character_moving
    global pil_pose_image
    global tkh_image
    global move_stop

    print("filename=",file.filename)
    result=200
    file_path= Path("./user_data/"+ user_name + "/"+ mode + "/")/ file.filename
    with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    input_image = Image.open(file_path)
    np_w_img = np.array(input_image, dtype=np.uint8)
    fd_image = cv2.cvtColor(np_w_img, cv2.COLOR_RGBA2BGRA)
    cv_w_img = cv2.cvtColor(fd_image, cv2.COLOR_BGRA2BGR)#Face detectのためにαチャンネルを削除
    print("input_image.shape[2]",input_image.mode)
    try:    
        _, dnum, predict_bbox, pre_dict_label_index, scores =AF.face_det_head(cv_w_img,1.0,1.0,0.5)#face-head検出   
        print("dnum=",dnum,"bbox=",predict_bbox,"label=",pre_dict_label_index,"score=",scores)
        mode=="tkh"
        if input_image.mode == "RGBA":
            pil_pose_image=input_image
        else:
            pil_pose_image,_=BG.del_bkg_out(input_image , "pil")
        tkh_image=pil_pose_image
        filename=file.filename.split(".")[0]+".png"
        img_base64 = get_base64_img(input_image)
        move_stop=True
    except:
        mode="bkg"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer) 
        img_backgraund = input_image
        img_base64 = get_base64_img(input_image)
        filename=file.filename
    start_mix_thread()
    return JSONResponse(content={'message': result,"filename": filename, "image": img_base64,"mode":mode,"character_moving":character_moving})

#キャラ設定
@app.post("/api/chr_def")
def chr_def(user_name: str = Form(...), chr_number: str = Form(...),chr_name: str =  Form(...),chr_data: str =  Form(...)):
    global chr1_data
    global chr2_data
    global chr1_name
    global chr2_name
    if chr_number=="1":
        if chr_data=="-":
            chr_data=chr1_data
        else:
            chr1_data=chr_data
        chr1_name=chr_name
        print("++++++++++++++++ chr1_data=",chr1_data)
    else:
        if chr_data=="-":
            chr_data=chr2_data
        else:
            chr2_data=chr_data
        chr2_name=chr_name
        print("++++++++++++++++ chr2_data=",chr2_data)
    return {"message":"updated","chr_data":chr_data}


#LLMとChat
@app.post("/api/chat")
def chat(user_txt: str =  Form(...), mode: str = Form("atbai"),user_name: str = Form(...),char_mode: str = Form("megu")):
    global l4_work
    global chr1_name
    global chr2_name

    if char_mode=="megu":
        chr_name=chr1_name
    else:
        chr_name=chr2_name
    l4_work=L4.image_past(l4_work,None,30,190,0.5)
    system_out = stabilityai(stb_url_local,user_txt,char_mode)
    posyl,l4_work = L4.ctx_mix(l4_work,bg_w,bg_h,system_out,char_mode,[40,0],chr_name,"user",user_txt)
    start_mix_thread()
    return JSONResponse(content={"answer_system":system_out})

#TTS
@app.post("/api/tts")
def tts(text: str =  Form(...), user_name: str = Form(...),char_mode: str = Form(...)):
    global audio_playng
    print("text=",text)
    print("char_mode=",char_mode)
    if char_mode=="megu":
        voice_id=2
    else:
        voice_id=8
    result,wav=tts_voce(text,voice_id)
    # 再生中スレッドが生きているかチェック
    while  audio_playng==True:
        print("再生中...")
        time.sleep(0.2)  # 0.2秒ごとにチェック
     # スレッドを作成して再生開始
    play_thread = threading.Thread(target=play_audio, args=(wav,))
    play_thread.start()
    audio_data = wav.raw_data  # Raw audio data
    return Response(content=audio_data, media_type="audio/wav")

# 再生を行う関数
def play_audio(audio_segment):
    global audio_playng
    audio_playng=True
    play(audio_segment)
    audio_playng=False

#Voice_mesasage get　
@app.post('/api/get_voice_msg')
def get_voice_msg(user_name: str = Form(...)):
    global voice_message
    global voice_new

    result="OK"
    if voice_new==True:
            out_msg=voice_message
            voice_new=False
    else:
            out_msg=""
    print('out_msg =', out_msg)
    return {"message":result,"voice":out_msg}

#voiceの開始と停止
@app.post('/api/get_voice_start')
def get_voice_start(user_name: str = Form(...), start_stop: str = Form(...)):
    global voice_thread
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",start_stop)

    if start_stop=="start":
        voice_thread=True
        get_voice_th1= threading.Thread(target=get_voice_th)
        get_voice_th1.start()
    else:
        voice_thread=False
    return {"message":"ok"}

# voice スレッド
def get_voice_th():
    global voice_message
    global voice_new
    global voice_thread
    print(host,port)
    # ソケットを用意
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((vhost, vport))
    while voice_thread:
        # 受信
        RXmsg, address = s.recvfrom(65535)
        msg=RXmsg.decode(encoding='utf-8')
        voice_message=f"{msg}"
        voice_new=True
        print(voice_message)
        print(f"message: {msg}\nfrom: {address}")

#anime Face move
@app.post("/api/tkh_move")
def tkh_move(user_name: str = Form(...), filename:str =  Form(...),move_type: str =  Form(...)):
    global move_stop
    global character_moving
    global fps

    user_id=0
    user_name="test"
    if move_type=="stop":
        move_stop=True

        return JSONResponse(content={'message':"stop","character_moving":character_moving})
    else:
        move_stop=False
    result = exec_pose(move_type,10,0.05,user_id,user_name) #キャラクタ動き制御開始
    return JSONResponse(content={'message': result,"character_moving":character_moving})

#Talking Head anime Face disp zoom
@app.post("/api/chara_zoom")
def chara_zoom(user_name: str = Form(...), mode:str =  Form(...)):
    global l3_scale
    global l3_pos
    global fps

    message="ok"

    if mode=="in":
        l3_scale -=0.05
        l3_pos[0] -=15
        #l3_pos[1] -=15        
    elif mode=="out":
        l3_scale +=0.05
        l3_pos[0] +=15
        #l3_pos[1] +=15 
    elif mode=="r":
        l3_pos[0] +=10
    elif mode=="l":
        l3_pos[0] -=10
    elif mode=="u":
        l3_pos[1] -=10
    elif mode=="d":
        l3_pos[1] +=10
    elif mode=="f":
        fps +=2
        if fps>50:
            fps=50
    elif mode=="s":
        fps -=2
        if fps<10:
            fps=10
    else :    
        message="ng"
    start_mix_thread()
    return JSONResponse(content={'message': message,"zoom_val":l3_scale})

#--------------------- 内部関数 ------------------------
def get_base64_img(image):
    # PILイメージをバイナリデータに変換
    img_io = io.BytesIO()
    image.save(img_io, format="PNG")
    img_io.seek(0)
    # 画像データをBase64エンコード
    return base64.b64encode(img_io.getvalue()).decode()
    
def randomname(n): #ランダムな文字列の生成
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

#---------------------   LLM   ------------------------

def stabilityai(url,user_prompt,char_mode,system="ユーザーの質問に答えなさい。"):
    if char_mode=="megu":
        #data = {"sys_msg" : """あなたは女子高校生の「めぐ」です。賢くて、おちゃめで、少しボーイッシュ、天真爛漫で好奇心旺盛な女子高生です。
        #    品川区の目黒川の近くで生まれました。いつも話言葉を使います。第一人称は「めぐ」と言いってください。「めぐ」のよく使う口癖は次のとおりです。
        #    その口癖に合わせた感じで話してください。みたいだ。そうなんだ。違うと思うけどね。だれ？。どこ？。""",
        #    "user_query":system,
        #    "user":user_prompt, 
        #    }
         data = {"user_query" : chr1_data,
            "sys_msg":system,
            "user":user_prompt, 
            }          
    else:
        #data = {"user_query" : """あなたは女子高校生の「さくら」です。賢くて、おちゃめで、少しボーイッシュ、天真爛漫で好奇心旺盛な女子高生です。
        #        豊中市の千里中央の近くで生まれました。いつも大阪弁の話言葉を使います。第一人称は「うち」と言いってください。「さくら」のよく使う口癖は次のとおりです。
        #        その口癖に合わせた感じで話してください。そやな。みたいやん。そうなん？。ちゃうと思うよ。だれなん？。知らんけど！。どこなん？。""",
        #    "sys_msg":system,
        #    "user":user_prompt, 
        #    } 
        data = {"user_query" : chr2_data,
            "sys_msg":system,
            "user":user_prompt, 
            }         

    # POSTリクエストを送信
    response = requests.post(url, json=data)
    # レスポンスを表示
    if response.status_code == 200:
        result = response.json()
        print("サーバーからの応答message:", result.get("message"))
        print("サーバーからの応答out:", result.get("out"))
    else:
        print("リクエストが失敗しました。ステータスコード:", response.status_code)
    return result.get("out")

def elz_13b(url,user_prompt,char_mode,system="ユーザーの質問に答えなさい。"):
    if char_mode=="megu":
        #data = {"user_query" : """あなたは女子高校生の「めぐ」です。賢くて、おちゃめで、少しボーイッシュ、天真爛漫で好奇心旺盛な女子高生です。
        #        品川区の目黒川の近くで生まれました。いつも話言葉を使います。第一人称は「めぐ」と言いってください。
        #        「めぐ」のよく使う口癖は次のとおりです。その口癖に合わせた感じで話してください。だよね。みたいだ。そうなんだ。違うと思うけどね。だれ？。どこ？。""",
        #    "sys_msg":system,
        #    "user":user_prompt, 
        #    }
         data = {"user_query" : chr1_data,
            "sys_msg":system,
            "user":user_prompt, 
            }     
    else:
        #data = {"user_query" : """あなたは女子高校生の「さくら」です。賢くて、おちゃめで、少しボーイッシュ、天真爛漫で好奇心旺盛な女子高生です。
        #        豊中市の千里中央の近くで生まれました。いつも大阪弁の話言葉を使います。第一人称は「うち」と言いってください。「さくら」のよく使う口癖は次のとおりです。
        #        その口癖に合わせた感じで話してください。そやな。みたいやん。そうなん？。ちゃうと思うよ。だれなん？。知らんけど！。どこなん？。""",
        #    "sys_msg":system,
        #    "user":user_prompt, 
        #    }
        data = {"user_query" : chr2_data,
            "sys_msg":system,
            "user":user_prompt, 
            }   
    # POSTリクエストを送信
    response = requests.post(url, json=data)
    # レスポンスを表示
    if response.status_code == 200:
        result = response.json()
        print("サーバーからの応答message:", result.get("message"))
        print("サーバーからの応答out:", result.get("out"))
    else:
        print("リクエストが失敗しました。ステータスコード:", response.status_code)
    return result.get("out")

# MIX thread single FOR TEST
def start_mix_thread():
    global running_threads

    while running_threads==True: #Lock時はlayer_mix_thを起動させない=layer_mix_thが動いている
        sleep(0.01)
        print("waiting for end of 'threads_mix_layer`")
    threads_mix_layer= threading.Thread(target=layer_mix_th)
    threads_mix_layer.start() #layer_mix_th開始

def layer_mix_th(): #frameに変化があるときだけに動くスレッド。　<=layer_mixing()で使う変数が変更されたときだけに呼び出されるのでCPU負荷が低い。
    global stream_image 
    global running_threads
 
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  layer_mix_th() @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    running_threads=True #Lock
    try:
        stream_image=layer_mixing()
    except:                                    
        print("layer_mixing() is not ready") 
    running_threads=False   #UNLock  終了

def layer_mixing():
    global pil_pose_image
    global l3_scale
    global l3_pos

    scale=l3_scale
    #l3ペースト
    try:
        back_im = img_backgraund.copy()
    except:
        print("backgraund is not exist")
        back_im=Image.open("white.png")
    #メイン・キャラクタペースト
    posx=int(l3_pos[0])
    posy=int(l3_pos[1])
    pil_pose_image_resize=pil_pose_image.resize((int(pil_pose_image.width //scale), int(pil_pose_image.height //scale)))
    try: #left-up X, left-up Y
        back_im.paste(pil_pose_image_resize,(posx,posy),pil_pose_image_resize)
    except:
        print("l3 is not pasted")#
    back_im.paste(l4_work,(0,0),l4_work) #ここでL4を重ねています。
    #CV2 イメージに変換
    back_im = np.array(back_im, dtype=np.uint8)
    back_im = cv2.cvtColor(back_im, cv2.COLOR_RGBA2BGRA)
    return back_im #最後の合成画像　CV2 イメージ

#---------------------------------------------------------- motion generation -------------------------------------------------------------------------
def exec_pose(move_type, dig,step, user_id,  user_name):
    global pil_pose_image
    global character_moving
    global move_stop
    global tkh_image
    global fps

    character_moving="moving"
    if move_type=="repeat":
        # 元の画像をロード
        original_image = tkh_image
        while True:
            angles = np.arange(0, dig, step)
            for angle in angles:
                start_time = time.time()
                # pil--> cv
                new_image = np.array(original_image, dtype=np.uint8)
                image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
                (h, w) = image.shape[:2]  # 画像の高さと幅を取得
                # 画像の中心を計算
                center = (w // 2, h // 2)
                # 回転に必要な行列を生成
                M = cv2.getRotationMatrix2D(center, angle, 1.0)  # 中心、角度、スケール
                # アフィン変換を使用して画像を回転
                rotated = cv2.warpAffine(image, M, (w, h))
                #cv --> pil
                new_image = cv2.cvtColor(rotated, cv2.COLOR_BGRA2RGBA)
                pil_pose_image = Image.fromarray(new_image)

                start_mix_thread()
    
                if (1/fps - (time.time()-start_time))>0:
                    sleep(1/fps - (time.time()-start_time))
                else:
                    print("Remain time is minus")
                print("Definec frame time=",'{:.2f}'.format((time.time()-start_time)*1000),"mS")
                if move_stop:
                    pil_pose_image = tkh_image
                    start_mix_thread()
                    break

            angles = np.arange(dig, -step, -step)
            for angle in angles:
                start_time = time.time()
                # pil--> cv
                new_image = np.array(original_image, dtype=np.uint8)
                image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
                (h, w) = image.shape[:2]  # 画像の高さと幅を取得
                # 画像の中心を計算
                center = (w // 2, h // 2)
                # 回転に必要な行列を生成
                M = cv2.getRotationMatrix2D(center, angle, 1.0)  # 中心、角度、スケール
                # アフィン変換を使用して画像を回転
                rotated = cv2.warpAffine(image, M, (w, h))
                #cv --> pil
                new_image = cv2.cvtColor(rotated, cv2.COLOR_BGRA2RGBA)
                pil_pose_image = Image.fromarray(new_image)

                start_mix_thread()

                if (1/fps - (time.time()-start_time))>0:
                    sleep(1/fps - (time.time()-start_time))
                else:
                    print("Remain time is minus")
                print("Definec frame time=",'{:.2f}'.format((time.time()-start_time)*1000),"mS")

                if move_stop:
                    break
            if move_stop:
                pil_pose_image = tkh_image
                start_mix_thread()
                break
    #サブプロセスの終了
    character_moving="stop"
    return "stop"

if __name__ == '__main__':
    uvicorn.run(app)