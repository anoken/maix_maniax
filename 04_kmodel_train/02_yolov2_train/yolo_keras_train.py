## Copyright (c) 2019 aNoken
import keras
from keras.models import Model
from keras.layers import Reshape,  Conv2D, Input
from keras.optimizers import Adam
import keras.backend as K
import tensorflow as tf
import numpy as np
import os, cv2
from yolo_utils.annotation import get_train_annotations
from yolo_utils.batch_gen import create_batch_generator
from yolo_utils.loss import YoloLoss
from mobilenet_sipeed.mobilenet_v1 import MobileNet

LABELS = ["target"]			#オブジェクトの名前

IMAGE_H, IMAGE_W = 224, 224		#画像のサイズ
GRID_H,  GRID_W  = 7 , 7		#確率MAPのサイズ
CLASS            = len(LABELS)		#検出オブジェクトの数
CLASS_WEIGHTS    = np.ones(CLASS, dtype='float32')#検出オブジェクトの確率
#アンカーボックス
ANCHORS          = [0.57273, 0.677385, 1.87446, 2.06253, 3.33843,
			 5.47434, 7.88282, 3.52778, 9.77052, 9.16828]	
BOX              = int(len(ANCHORS)/2)		#アンカーボックスの大きさ
BATCH_SIZE       = 16				#学習データを小分けにする数

#学習に使うデータセットの格納場所
train_image_folder = './Dataset/image/train/'
train_annot_folder = './Dataset/annotation/train/'
valid_image_folder = ''
valid_annot_folder = ''

#MobileNetベースのYOLOv2のモデルを作成
input_image = Input(shape=(IMAGE_H, IMAGE_W, 3))

mobilenet = MobileNet(input_shape=(IMAGE_H,IMAGE_W,3),
 alpha = 0.75,depth_multiplier = 1, dropout = 0.001, include_top=False,
 weights = 'imagenet', classes = 1000,  backend=keras.backend,
  layers=keras.layers,models=keras.models,utils=keras.utils)

feature_extractor = mobilenet(input_image)
output_tensor = Conv2D(BOX * (4 + 1 + CLASS), (1,1), strides=(1,1),
                       padding='same', 
                       name='detection_layer_{}'.format(BOX * (4 + 1 + CLASS)), 
                       kernel_initializer='lecun_normal')(feature_extractor)

output_tensor = Reshape((GRID_H, GRID_W, BOX, 4 + 1 + CLASS))(output_tensor)
model = Model(input_image, output_tensor)

#学習をしていないレイヤーの重みを初期化
layer = model.layers[-2]
weights = layer.get_weights()
new_kernel = np.random.normal(size=weights[0].shape)/(IMAGE_H*IMAGE_W)
new_bias   = np.random.normal(size=weights[1].shape)/(IMAGE_H*IMAGE_W)
layer.set_weights([new_kernel, new_bias])

model.summary()

#画像とアノテーションをバッチ化

train_times=1	#学習を繰り返す回数
valid_times=1	#訓練を繰り返す回数
jitter=True	#学習画像をX,Y方向に動かしてノイズを与える

def normalize(image): 
    image = image / 255. 
    image = image - 0.5 
    image = image * 2. 
    return image
    
    
train_annotations, valid_annotations = get_train_annotations(LABELS,train_image_folder,train_annot_folder,valid_image_folder,valid_annot_folder)

train_batch_generator = create_batch_generator(train_annotations,IMAGE_H,GRID_H,BATCH_SIZE,ANCHORS,train_times,jitter=jitter,norm=normalize)
                                         
valid_batch_generator = create_batch_generator(valid_annotations,IMAGE_H,GRID_H,BATCH_SIZE,ANCHORS,train_times,jitter=jitter,norm=normalize)

#損失関数と最適化アルゴリズムの設定

#アンカーボックスのオブジェクトのある部分の予測誤差にペナルティを科す係数
NO_OBJECT_SCALE  = 1.0	
#アンカーボックスのオブジェクトのない部分の予測誤差にペナルティを科す係数
OBJECT_SCALE     = 5.0	
#位置とサイズの予測（x、y、w、h）の誤差にペナルティを科す係数
COORD_SCALE      = 1.0	
#クラス予測の誤差にペナルティを科す係数
CLASS_SCALE      = 1.0	

yolo_loss = YoloLoss(GRID_H,CLASS,ANCHORS,COORD_SCALE,CLASS_SCALE,
                     OBJECT_SCALE,NO_OBJECT_SCALE)
custom_loss = yolo_loss.custom_loss(BATCH_SIZE)
optimizer = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss=custom_loss, optimizer=optimizer)

# 学習開始
history=model.fit_generator(generator        = train_batch_generator, 
                    steps_per_epoch  = len(train_batch_generator), 
                    validation_data  = valid_batch_generator,
                    validation_steps = len(valid_batch_generator),
                    epochs           = 50, 
                    verbose          = 1,
                    max_queue_size   = 3)



#Kerasモデル形式で保存
output_node_names = [node.op.name for node in model.outputs]
input_node_names = [node.op.name for node in model.inputs]
output_layer = model.layers[2].name+'/BiasAdd'
model.save("my_yolo.h5",include_optimizer=False)

#Keras->TensorFlowLite形式に変換
converter = tf.lite.TFLiteConverter.from_keras_model_file("my_yolo.h5",output_arrays=[output_layer])
tflite_model = converter.convert()
open('my_yolo.tflite', "wb").write(tflite_model)

#TensorFlowLite->kmodel形式に変換
import subprocess
subprocess.run(['./ncc/ncc','my_yolo.tflite','my_yolo.kmodel'
,'-i','tflite','-o','k210model','--dataset','images'])

