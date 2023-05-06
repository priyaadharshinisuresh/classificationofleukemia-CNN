# -*- coding: utf-8 -*-
"""LeukemiaNet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MV5YNzgMOchb8aOP97B9PYEToQzKb3L2
"""
import matplotlib.pyplot as plt
import os
import PIL
import numpy as np
import tensorflow as tf
from keras import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.models import * 
from tensorflow.keras.preprocessing import image

print(tf.__version__)
print(tf.keras.__version__)

from google.colab import drive
drive.mount('/content/drive')

train_datagen = image.ImageDataGenerator(
    rotation_range=15,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1)
test_datagen= image.ImageDataGenerator(
    rotation_range=15,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1)

train_generator = train_datagen.flow_from_directory("/content/drive/MyDrive/Final Review/dataset20/train",
    target_size = (224,224),
    batch_size = 4,
    class_mode = 'categorical') # 'categorical'
validation_generator = test_datagen.flow_from_directory("/content/drive/MyDrive/Final Review/dataset20/test",
    target_size = (224,224),
    batch_size = 4,
    class_mode = 'categorical')  # 'categorical'

import tensorflow as tf
base_model = tf.keras.applications.EfficientNetB3(weights='imagenet', input_shape=(224,224,3), include_top=False)
for layer in base_model.layers:
    layer.trainable=False
model = Sequential()
model.add(base_model)
model.add(Conv2D(filters=64,kernel_size=(3,3),activation='relu'))
model.add(GaussianNoise(0.25))
model.add(GlobalAveragePooling2D())
model.add(Dense(512,activation='relu'))
model.add(Dropout(0.25))
model.add(GaussianNoise(0.25))
model.add(Dense(5, activation='softmax'))  
model.summary()

model.compile(loss='categorical_crossentropy', 
              optimizer='adam',
              metrics=['accuracy','Precision','Recall','AUC'])

import tensorflow as tf
base_model = tf.keras.applications.VGG16(weights='imagenet', input_shape=(224,224,3), include_top=False)
for layer in base_model.layers:
    layer.trainable=False
model1 = Sequential()
model1.add(base_model)
model1.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
model1.add(GaussianNoise(0.35))
model1.add(GlobalAveragePooling2D())
#model.add(Dense(256,activation='relu'))
model1.add(Dense(512,activation='relu'))
model1.add(BatchNormalization())
model1.add(GaussianNoise(0.35))
model1.add(Dropout(0.35))
model1.add(Dense(5, activation='softmax'))
model1.summary()

model1.compile(loss='categorical_crossentropy', 
              optimizer='adam',
              metrics=['accuracy','Precision','Recall','AUC'])

from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Average
model = load_model('/content/drive/MyDrive/Final Review/model1.h5')
model = Model(inputs=model.inputs,
                outputs=model.outputs,
                name='name_of_model')
model1 = load_model('/content/drive/MyDrive/Final Review/model2.h5')
model1 = Model(inputs=model1.inputs,
                outputs=model1.outputs,
                name='name_of_model1')
models = [model, model1]
model_input = Input(shape=(224, 224, 3))
model_outputs = [model(model_input) for model in models]
ensemble_output = Average()(model_outputs)
ensemble_model = Model(inputs=model_input, outputs=ensemble_output, name='ensemble')

ensemble_model.compile(loss='categorical_crossentropy', 
              optimizer='adam',
              metrics=['accuracy','Precision','Recall','AUC'])

model=tf.keras.models.load_model('/content/drive/MyDrive/Final Review/LeukemiaNet.h5')

#! pip install streamlit

#!pip install -U ipykernel

#!pip install pyngrok

#from pyngrok import ngrok

#ngrok.set_auth_token("2NmqkCBhaz9UBEWvfo8AHqi5L6b_256Nk38CRrassvcXLN6fi")

# Commented out IPython magic to ensure Python compatibility.
#%%writefile app.py

import streamlit as st


st.set_option('deprecation.showfileUploaderEncoding', False)
@st.cache(allow_output_mutation=True)
def load_model():
   model=tf.keras.models.load_model('/content/drive/MyDrive/Final Review/LeukemiaNet.h5')
   return model
model=load_model()
st.write("""
          # Leukemia Classification
          """
          )
file = st.file_uploader("Please upload an blood smear image file", type=["jpg", "png"])
import cv2
from PIL import Image, ImageOps
import numpy as np
def import_and_predict(image_data, model):
     
         size = (224,224)    
         image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
         image = np.asarray(image)
         img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
         img_resize = (cv2.resize(img, dsize=(75, 75),    interpolation=cv2.INTER_CUBIC))/255.
         
         img_reshape = img[np.newaxis,...]
     
         ypred = model.predict(img_reshape)
         
         return ypred
if file is None:
     st.text("Please upload an image file")
else:
     image = Image.open(file)
     st.image(image, use_column_width=True)
     ypred = import_and_predict(image, model)
     class_names=['ALL-Acute Lymphocytic Leukemia', 'AML-Acute Myelogenous Leukemia ', 'CLL-Chronic Lymphocytic Leukemia', 'CML-Chronic Myelogenous Leukemia ', 'NORMAL']
     string= "This image belongs to : "+class_names[np.argmax(ypred)]
     st.success(string)
 
