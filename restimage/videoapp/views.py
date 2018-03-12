from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from .models import VideoSign
from .serializers import VideoSignSerializer  
import json

# Create your views here.
import sys
import os
import numpy as np
import copy
import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf


def predict(sess,softmax_tensor,label_lines,image_data):

    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
#image_path= "C:\Users\Shushant Kumar\Documents\GitHub\DjangoImage\media_cdn\A3.jpg"
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

    max_score = 0.0
    res = ''
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        if score > max_score:
            max_score = score
            res = human_string
    return res, max_score

def videoClassify(serializer):
	video_name=serializer.data['id']
	vide = VideoSign.objects.get(id=video_name)
	video_path= vide.video.path
	print(video_path)
	main_path=video_path[:(len(video_path)-len(vide.video.name))]
	log_path = main_path+"logs\output_labels.txt"

	# Loads label file, strips off carriage return
	label_lines = [line.rstrip() for line
	                   in tf.gfile.GFile(log_path)]

	graph_path = main_path + "logs\output_graph.pb"

	# Unpersists graph from file
	with tf.gfile.FastGFile(graph_path, 'rb') as f:
	    graph_def = tf.GraphDef()
	    graph_def.ParseFromString(f.read())
	    _ = tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
	    # Feed the image_data as input to the graph and get first prediction
	    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

	    c = 0

	    cap = cv2.VideoCapture(video_path)

	    res, score = '', 0.0
	    i = 0
	    mem = ''
	    consecutive = 0
	    sequence = ''
	    result = {}
	    while True:
	        ret, img = cap.read()
	        img = cv2.flip(img, 1)
	        if ret:
	            x1, y1, x2, y2 = 100, 100, 300, 300
	            img_cropped = img[y1:y2, x1:x2]

	            c += 1
	            image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()
	            a = cv2.waitKey(33)
	            if i == 4:
	                res_tmp, score = predict(sess,softmax_tensor,label_lines,image_data)
	                res = res_tmp
	                i = 0
	                if mem == res:
	                    consecutive += 1
	                else:
	                    consecutive = 0
	                if consecutive == 2 and res not in ['nothing']:
	                    if res == 'space':
	                        sequence += ' '
	                    elif res == 'del':
	                        sequence = sequence[:-1]
	                    else:
	                        sequence += res
	                    consecutive = 0
	            i += 1
	            k = float(score)
	            z = res.upper()
	            local = { z:k }
	            result.update(local)
	            # cv2.putText(img, '%s' % (res.upper()), (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
	            # cv2.putText(img, '(score = %.5f)' % (float(score)), (100,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
	            mem = res
	            # cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
	            # cv2.imshow("img", img)
	            # img_sequence = np.zeros((200,1200,3), np.uint8)
	            # cv2.putText(img_sequence, '%s' % (sequence.upper()), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
	            # cv2.imshow('sequence', img_sequence)
	        else:
	            break
	return result



class VideoSignList(APIView):

	def get(self,request):
		stocks = VideoSign.objects.all() 
		serializer = VideoSignSerializer(stocks, many = True)
		return Response(serializer.data)

		

	def post(self,request):
		serializer = VideoSignSerializer(data=request.data)

		
		if serializer.is_valid():
			serializer.save()

			#console.log(score)
			requ = videoClassify(serializer)
			#requ = json.dumps(requ)

			vid_name = serializer.data['id']
			snippet = VideoSign.objects.get(id= vid_name)
			# comment below line to store the posted imageClassify 
			snippet.delete()
			return Response(requ, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)