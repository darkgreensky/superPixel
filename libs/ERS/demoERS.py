import time

from .ERSModule import *
import cv2
import numpy as np

def ERS_handle(img, nC=100):
	img_list = img.flatten().tolist()
	h = img.shape[0]
	w = img.shape[1]
	grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# print grayImg.shape
	start_time = time.time()
	label_list = ERS(img_list, h, w, nC)
	end_time = time.time()
	label = np.reshape(np.asarray(label_list), (h, w))
	return label, end_time - start_time
