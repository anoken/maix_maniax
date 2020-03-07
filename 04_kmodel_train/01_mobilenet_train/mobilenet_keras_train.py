## Copyright (c) 2019 aNoken

import keras,os
import numpy as np
from keras import backend as K, Sequential
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils
from keras.layers import Dense, GlobalAveragePooling2D, Dropout,Input
from keras.applications.mobilenet import preprocess_input
import tensorflow as tf
from mobilenet_sipeed.mobilenet_v1 import MobileNet
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
TRAINING_DIR = 'dataset/train_temp'
VALIDATION_DIR = 'dataset/train_temp'
EPOCHS=20

# 画像データの読み込み
imageGen=ImageDataGenerator(preprocessing_function=preprocess_input,validation_split = 0.2)
batch_size=128

train_generator=imageGen.flow_from_directory(TRAINING_DIR,
	target_size=(IMAGE_WIDTH,IMAGE_HEIGHT),color_mode='rgb',
	batch_size=batch_size,class_mode='categorical', shuffle=True, subset = "training")

validation_generator=imageGen.flow_from_directory(VALIDATION_DIR,
	target_size=(IMAGE_WIDTH,IMAGE_HEIGHT),color_mode='rgb',
	batch_size=batch_size,class_mode='categorical', shuffle=True,subset = "validation")

NUM_CLASSES=len(train_generator.class_indices)

# MobileNetモデルの読み込み
input_image = Input(shape=(IMAGE_WIDTH, IMAGE_HEIGHT, 3))
mobilenet=MobileNet(input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, 3), alpha = 0.75,depth_multiplier = 1,
 dropout = 0.001,include_top = False, weights = "imagenet", classes = 1000, backend=keras.backend, 
 layers=keras.layers,models=keras.models,utils=keras.utils)

# 出力層の追加
x = mobilenet(input_image)
x=GlobalAveragePooling2D()(x)
x=Dense(100,activation='relu')(x)#
x=Dropout(0.1)(x)
x=Dense(50, activation='relu')(x)
preds=Dense(NUM_CLASSES, activation='softmax')(x)

mbnetModel=Model(inputs=input_image,outputs=preds)

for i,layer in enumerate(mbnetModel.layers):
    print(i,layer.name)

for layer in mobilenet.layers:
    layer.trainable = False

# モデル構成の表示
mbnetModel.summary()

# アルゴリズムを設定
mbnetModel.compile(optimizer='Adam',loss='categorical_crossentropy',
metrics=['accuracy'])

step_size_train = (train_generator.n//train_generator.batch_size)
validation_steps = (validation_generator.n//train_generator.batch_size)


# 途中経過を保存する
class Callback(tf.keras.callbacks.Callback):
    def on_epoch_end(self,epoch, logs=None):
        mbnetModel.save("weight.h5")

cb = Callback()
initial_epoch = 0

if os.path.isfile(os.path.join("weight.h5")):    
    mbnetModel.load_weights(os.path.join("weight.h5"))

# 学習開始

history=mbnetModel.fit_generator(generator=train_generator, 
	steps_per_epoch=step_size_train, epochs=EPOCHS, 
	validation_data = validation_generator,validation_steps = validation_steps,
	verbose = 1,callbacks=[cb])



#Confusion Matrixの作成
validation_data=validation_generator

validation_data.reset()
validation_data.shuffle = False
validation_data.batch_size = 1

predicted = mbnetModel.predict_generator(validation_data, steps=validation_data.n)
predicted_classes = np.argmax(predicted, axis=-1)

cm = confusion_matrix(validation_data.classes, predicted_classes)
print(cm)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
plt.figure(figsize=(12, 9))
sns.heatmap(cm, annot=True, square=True, cmap=plt.cm.Blues,
            xticklabels=validation_data.class_indices,
            yticklabels=validation_data.class_indices)
plt.title("Confusion Matrix")
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()
plt.savefig('./confusion_matrix.png')

#Kerasモデル形式で保存
mbnetModel.save('my_mbnet.h5')

#Keras->TensorFlowLite形式に変換
converter = tf.lite.TFLiteConverter.from_keras_model_file('my_mbnet.h5')
tflite_model = converter.convert()
open('my_mbnet.tflite', "wb").write(tflite_model)

#TensorFlowLite->kmodel形式に変換
import subprocess
subprocess.run(['./ncc/ncc','my_mbnet.tflite','my_mbnet.kmodel','-i',
'tflite','-o','k210model','--dataset','images'])

