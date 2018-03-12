from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from .models import VideoStream
from .serializers import VideoStreamSerializer  
import json

# Create your views here.
import tensorflow as tf
import sys
import os
import cv2
import numpy
# Disable tensorflow compilation warnings

def imageClassify(request):
	os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

	# #image_path = '..\..\media\p1.jpg'
	# image_name=serializer.data['id']
	# # image_file=serializer.data['image']
	# # print(image_file)

	# phot = Stock.objects.get(id=image_name)
	# #phot = Stock.objects.get(name='A3')
	# #print(image_name)

	# image_path= phot.image.path
	# image_path= "C:\Users\Shushant Kumar\Documents\GitHub\DjangoImage\media_cdn"
	# print(image_path)
	#image_path="http://localhost:8000/media/p7.jpg"
	# image_data = tf.gfile.FastGFile(image_path, 'rb').read()
	print("here1")
	image_data = request
	print("here2")
	# label_lines = [line.rstrip() for line
	#                    in tf.gfile.GFile("logs/output_labels.txt")]
	#print(image_path)
	
	# main_path=image_path[:(len(image_path)-len(phot.image.name))]
	
	log_path = "C:\\Users\\Shushant Kumar\\Documents\\GitHub\\DjangoImage\\media_cdn\\logs\\output_labels.txt"
	#print(log_path)
	label_lines = [line.rstrip() for line
	                   in tf.gfile.GFile(log_path)]
	print("here3")

	# Unpersists graph from file
	graph_path = "C:\\Users\\Shushant Kumar\\Documents\\GitHub\\DjangoImage\\media_cdn\\logs\\output_graph.pb"
	#print(graph_path)
	with tf.gfile.FastGFile(graph_path, 'rb') as f:
	    graph_def = tf.GraphDef()
	    graph_def.ParseFromString(f.read())
	    _ = tf.import_graph_def(graph_def, name='')

	print("here4")

	with tf.Session() as sess:
	    # Feed the image_data as input to the graph and get first prediction
	    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

	    predictions = sess.run(softmax_tensor, \
	             {'DecodeJpeg/contents:0': image_data})

	    # Sort to show labels of first prediction in order of confidence
	    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
	    result = {}
	    for node_id in top_k:
	    	human_string = label_lines[node_id]
	    	score = predictions[0][node_id]
	    	local = {human_string:score}
	    	result.update(local)

	return result


class StreamList(APIView):

	# def get(self,request):
	# 	stocks = VideoStream.objects.all() 
	# 	serializer = VideoStreamSerializer(stocks, many = True)
	# 	return Response(serializer.data)

		

	def post(self,request):
		print(request)
		# print(request.file)
		requ = imageClassify(request)
		# print(request.data)
		# return Response("Received", status=status.HTTP_201_CREATED)
		# serializer = VideoStreamSerializer(data=request.data)

		
		# if serializer.is_valid():
		# 	serializer.save()

		# 	#console.log(score)
		# 	requ = videoClassify(serializer)
		# 	#requ = json.dumps(requ)

		# 	img_name = serializer.data['id']
		# 	snippet = VideoStream.objects.get(id= img_name)
		# 	# comment below line to store the posted imageClassify 
		# 	snippet.delete()
		return Response(requ, status=status.HTTP_201_CREATED)
		# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
