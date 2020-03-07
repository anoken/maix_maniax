## Copyright (c) 2019 aNoken

import sensor,image,lcd,time 
import KPU as kpu
from Maix import FPIOA,GPIO,utils
from fpioa_manager import fm
from board import board_info

print(kpu.memtest())
task_fd = kpu.load(0x200000) #顔検出モデルのロード
task_ld = kpu.load(0x300000) #顔に5ポイントキーポイント検出モデルを読み込む
task_fe = kpu.load(0x400000) #顔の196次元の固有値モデルを読み込む
print(kpu.memtest())

clock = time.clock()            #システムクロックを初期化し、フレームレートを計算する

fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)    #設定ボタンピン
key_gpio=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

last_key_state=1
key_pressed=0               #キーピンを初期化する
def check_key():    		#キー検出機能
    global last_key_state
    global key_pressed
    val=key_gpio.value()
    if last_key_state == 1 and val == 0:
        key_pressed=1
    else:
        key_pressed=0
    last_key_state = val

lcd.init()      #LCD初期化
lcd.rotation(0) #センサーカメラを初期化する
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)   #カメラミラーリングの設定
sensor.set_vflip(1)     #カメラのフリップを設定する
sensor.run(1)           #カメラを有効にする

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 
6.92275, 6.718375, 9.01025)
#顔検出用アンカー

#顔の5つのキーポイント座標、左目、右目、鼻、左口の角、右口の角
dst_point = [(44,59),(84,59),(64,82),(47,105),(81,105)] 

a = kpu.init_yolo2(task_fd, 0.5, 0.3, 5, anchor)    #顔検出モデルを初期化する
img_lcd=image.Image()			#表示バッファを設定
img_face=image.Image(size=(128,128))	#顔画像バッファを設定
a=img_face.pix_to_ai()			#画像をkpuの形式に変換
record_ftr=[]			#196次元の特徴ベクトル保存用のリスト
record_ftrs=[]			#顔の特徴の主要な特徴を保存する
names = ['Mr.1', 'Mr.2', 'Mr.3', 'Mr.4', 'Mr.5', 'Mr.6', 'Mr.7', 
'Mr.8', 'Mr.9' , 'Mr.10']	#人名タグ。

while(1):
    check_key()			#キー検出
    img = sensor.snapshot()	#カメラから写真を取得する
    clock.tick()	#記録時間、フレームレートの計算に使用
    code = kpu.run_yolo2(task_fd, img)	#顔検出で座標位置を取得
    if code:	#顔が検出された場合
        for i in code:		#反復座標ボックス
        
            #顔をカットし、128x128にサイズ変更
            a = img.draw_rectangle(i.rect())	#画面に顔枠を表示

            #画像の顔の部分をface_cutに切り抜く
            face_cut=img.cut(i.x(),i.y(),i.w(),i.h())	
            #トリミングされた顔画像を128 * 128ピクセルに拡大縮小
            face_cut_128=face_cut.resize(128,128)
			#推測された画像をkpuで受け入れられる形式に変換
            a=face_cut_128.pix_to_ai()
            
           	#顔キーポイント検出
            fmap = kpu.forward(task_ld, face_cut_128)
            plist=fmap[:]
          
          	#左眼の位置
            le=(i.x()+int(plist[0]*i.w()-10),i.y()+int(plist[1]*i.h()))  
			#右眼位置
            re=(i.x()+int(plist[2]*i.w()),i.y()+int(plist[3]*i.h())) 
            #鼻位置
            nose=(i.x()+int(plist[4]*i.w()),i.y()+int(plist[5]*i.h()))
            #左口位置
            lm=(i.x()+int(plist[6]*i.w()),i.y()+int(plist[7]*i.h()))
            #右口位置
            rm=(i.x()+int(plist[8]*i.w()),i.y()+int(plist[9]*i.h()))

            #対応する位置に小さな円を描く
            a = img.draw_circle(le[0], le[1], 4)
            a = img.draw_circle(re[0], re[1], 4)
            a = img.draw_circle(nose[0], nose[1], 4)
            a = img.draw_circle(lm[0], lm[1], 4)
            a = img.draw_circle(rm[0], rm[1], 4)	
            
            
            #顔を標準位置に合わせる
            src_point = [le, re, nose, lm, rm]	#画像内の5座標位置
            
            ＃取得した5点座標と標準の正の顔座標に基づいてアフィン変換行列を取得
            T=image.get_affine_transform(src_point, dst_point)
            
            ＃元の顔画像をアフィン変換してポジティブな顔画像に変換する
            a=image.warp_affine_ai(img, img_face, T)
            
            ＃正の顔画像をkpu形式に変換
            a=img_face.ai_to_pix()
            del(face_cut_128)	#切り抜いた顔の写真をリリース
            
			#顔画像の196次元の特徴量を計算する
            fmap = kpu.forward(task_fe, img_face)
            feature=kpu.face_encode(fmap[:])
            reg_flag = False
            
         	#現在の顔の特徴値と保存されている特徴値のスコアを計算します
            scores = []		
            for j in range(len(record_ftrs)):
                score = kpu.face_compare(record_ftrs[j], feature)
                scores.append(score)
            max_score = 0
            index = 0
            
            #最大スコアとインデックス値を検索
            for k in range(len(scores)):	
                if max_score < scores[k]:
                    max_score = scores[k]
                    index = k
                    
            #最大スコアが85より大きい場合、同じ人とみなす
            if max_score > 85:	
            	#名前とスコアを表示する
                a = img.draw_string(i.x(),i.y(), 
                	("%s :%2.1f" % (names[index], max_score)),
                	 color=(0,255,0),scale=2)
            else:
            	#不明対スコアを表示
                a = img.draw_string(i.x(),i.y(),
                	 ("X :%2.1f" % (max_score)), color=(255,0,0),scale=2)
                	 
            if key_pressed == 1:	
	            #現在の機能を既知の機能のリストに追加します
                key_pressed = 0		
                record_ftr = feature
                record_ftrs.append(record_ftr)
            break
    fps =clock.fps()
    a = lcd.display(img)
