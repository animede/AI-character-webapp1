
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
global ctx_l4
global img_llm

class  Draw_l4:
    def __init__(self,url,w,h):
        global ctx_l4
        global img_llm
        self.url=url
        ctx_l4=Image.new('RGBA', (w, h), (0, 0, 0, 0))
        img_llm=Image.new('RGBA', (w, h), (0, 0, 0, 0))

    def ctx_mix(self,l4_img,w,h, ctx_txt,char_mode,ctx_pos,chr_name, user="",user_txt="", ctx_up_dw="down", ctx_font='RictyDiminished-Regular.ttf',ctx_font_size=20,ctx_color='#000000',ctx_edge_width=2,ctx_edge_color="#ffffff"):
    #def ctx_mix(self,l4_img,w,h, ctx_txt,ctx_up_dw="down", ctx_pos=[40,148], ctx_font='RictyDiminished-Regular.ttf',ctx_font_size=20,ctx_color='#000000',ctx_edge_width=2,ctx_edge_color="#ffffff"):
        global ctx_l4
        w, h = l4_img.size
        l4_ctx= Image.new('RGBA', (w, h), (0, 0, 0, 0))#クリア画像を作成
        ctx_font_path='./font/'+ ctx_font
        ctx_font= ImageFont.truetype(ctx_font_path, ctx_font_size)
        font_color = ctx_color
        print("キャラ会話ペースト:", ctx_txt)
        # 改行をコンマに置換
        ctx_txt = ctx_txt.replace("\n", ",")  # 置換結果を再代入
        # テキストを描画する位置
        posx = int(ctx_pos[0])
        posy = int(ctx_pos[1])
        # 1行に表示可能な文字数
        ctx_line_chr_num = int((w/2 - posx) / ctx_font_size)
        ctx_list = []
        # テキストを行ごとのリストに分割
        for line in range(int(len(ctx_txt) / ctx_line_chr_num) + 1):
            ctx_list.append(ctx_txt[line * ctx_line_chr_num: line * ctx_line_chr_num + ctx_line_chr_num])
        user_list = []
        for line in range(int(len(user_txt) / ctx_line_chr_num) + 1):
            user_list.append(user_txt[line * ctx_line_chr_num: line * ctx_line_chr_num + ctx_line_chr_num])
        print("キャラ会話LIST:", ctx_list)
        # ImageDrawオブジェクトを一度だけ作成
        draw = ImageDraw.Draw(l4_ctx)
        # テキストの描画
        #current_line = len(ctx_list)
        if ctx_up_dw == "up":
            for i in range(1, current_line + 1):
                posyl = posy - i * ctx_font_size+3
                ctxpos = (posx, posyl)
                draw.multiline_text(ctxpos, ctx_list[current_line - i], font=ctx_font, fill=font_color, stroke_width=ctx_edge_width, stroke_fill=ctx_edge_color)
        else:  # "down"
            posy=posy+35
            ctxpos = (posx, posy)
            if  user=="user":
                
                name="■■■"+"ユーザ"+"■■■"
                chr_color="#00ff00"
                draw.multiline_text(ctxpos, name, font=ctx_font, fill=chr_color, stroke_width=ctx_edge_width, stroke_fill=ctx_edge_color)
                posy=posy+20
                current_line = len( user_list)
                for i in range(current_line):
                    posyl = posy + i * ctx_font_size+3
                    ctxpos = (posx, posyl)
                    try:
                        draw.multiline_text(ctxpos, user_list[i], font=ctx_font, fill=font_color, stroke_width=ctx_edge_width, stroke_fill=ctx_edge_color)
                    except Exception as e:
                        print(f"ctx_txt draw error: {e}")
            posy=posyl+30
            if char_mode=="megu":
                chr_name_tab="■■■"+chr_name+"■■■"
                chr_color="#00FFFF"
            elif char_mode=="sakura":
                chr_name_tab="■■■"+chr_name+"■■■"
                chr_color="#FF1493"
            ctxpos = (posx, posy)
            draw.multiline_text(ctxpos, chr_name_tab, font=ctx_font, fill=chr_color, stroke_width=ctx_edge_width, stroke_fill=ctx_edge_color)
            posy=posy+20
            ctxpos = (posx, posy)
            current_line = len(ctx_list)
            for i in range(current_line):
                posyl = posy + i * ctx_font_size+3
                ctxpos = (posx, posyl)
                try:
                    draw.multiline_text(ctxpos, ctx_list[i], font=ctx_font, fill=font_color, stroke_width=ctx_edge_width, stroke_fill=ctx_edge_color)
                except Exception as e:
                    print(f"ctx_txt draw error: {e}")
        ctx_l4=l4_ctx
        l4 = self.mx_l4()
        return posyl,l4

    def image_past(self,l4,img,img_w=100,img_h=100,scale=0.5):
        global img_llm
        w,h=l4.size
        l4_llm= Image.new('RGBA', (w, h), (0, 0, 0, 0))#クリア画像を作成
        if img!=None:
            wp,hp=img.size
            if w < h:
                scale= (h*0.5)/hp
                if wp*scale > w*0.5:
                    scale=(w*0.5)/wp
            elif wp<hp+1:
                scale=(h*0.6)/hp
                if hp*scale>h*0.6:
                    scale=(h*0.6)/hp
            else:
                scale=(w*0.5)/wp
                if wp*scale>w*0.5:
                    scale=(w*0.5)/wp
                elif hp*scale>h*0.55:
                    scale=(h*0.6)/hp
            size = (round(img.width * scale), round(img.height * scale))
            img_resize=img.resize(size)
            
            new_w=img_resize.width+10
            new_h=img_resize.height+10
            new_image = Image.new("RGB", (new_w, new_h), "white")
            new_image.paste(img_resize,(5,5))
            l4_llm.paste(new_image, (img_w,img_h))
        
        img_llm=l4_llm
        l4 = self.mx_l4()
        return l4
    
    def mx_l4(self):
        global ctx_l4
        global img_llm

        mixed_l4 = Image.alpha_composite(ctx_l4, img_llm)
        
        return mixed_l4
