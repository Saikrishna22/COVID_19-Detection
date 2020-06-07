import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
import pickle
from sklearn.externals import joblib 
import joblib 
import pickle
import keras
import json
from keras.models import Model, load_model,model_from_json
import tensorflow.compat.v1 as tf

with open("body.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Covid-19 Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: red;'>Only for Research Purpose</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: right; color: red;'>Saikrishna R</p>", unsafe_allow_html=True)
def main():
	
	
	html_temp = """
	<div style= "background-color:yellow;">
	<p>  </p>
	</div>
	"""
	k=0
	st.markdown(html_temp,unsafe_allow_html = True)
	# st.title('Covid-19 Prediction')
	# st.text('Select an option')
	# page = st.sidebar.selectbox("Choose a page", [' ','Covid Prediction','Covid Segmentation'])	
	page = st.selectbox("Select an option", [' ','Covid Prediction','Covid Segmentation'],key='button')	
	if page == 'Covid Prediction':
		uploaded_file = st.file_uploader("Upload Image")
		

		if uploaded_file is not None:	
			image = Image.open(uploaded_file)
			st.image(image, caption='Input',width = 300)
			# subpage = st.selectbox("predict", ['predict'])
			if st.button('predict'):
				img_array = np.array(image)
				print('img_array',img_array.shape)
				resize_img = cv2.resize(img_array  , (224 , 224))
				print('ssopencv',resize_img.shape)	
				img = np.reshape(resize_img,[1,224,224,3])
				print(img.shape)
				with open('model_config1.json') as json_file:
					json_config = json_file.read()
				new_model = tf.keras.models.model_from_json(json_config)
				new_model.load_weights('Model_vgg_224_25e_adam_weights.h5')
				# print('hello')
				p = new_model.predict([img])
				label_pickle = 'label_transform_covid.pkl'
				with open(label_pickle, 'rb') as file:
					label = pickle.load(file)
				y_classes = p.argmax(axis=-1)
				x = label.classes_[y_classes]
				if x[0]=='CT_COVID':
					st.subheader('COVID POSITIVE')
				else:
					st.subheader('COVID NEGATIVE')


if __name__ == '__main__':
	import tensorflow.compat.v1 as tf
	tf.disable_v2_behavior()
	main()



	