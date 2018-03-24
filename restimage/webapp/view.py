#from django.conf.settings import PROJECT_ROOT
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from .models import Stock
from .serializers import StockSerializer  
import json

# Create your views here.

import tensorflow as tf
import sys
import os
# Disable tensorflow compilation warnings

def imageClassify(serializer):
	os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

	#image_path = '..\..\media\p1.jpg'
	image_name=serializer.data['id']
	# image_file=serializer.data['image']
	# print(image_file)
	print(image_name)

	phot = Stock.objects.get(id=image_name)
	#phot = Stock.objects.get(name='A3')
	#print(image_name)

	image_path= phot.image.path
	#image_path= "C:\Users\Shushant Kumar\Documents\GitHub\DjangoImage\media_cdn\A3.jpg"
	print(image_path)
	#image_path="http://localhost:8000/media/p7.jpg"
	image_data = tf.gfile.FastGFile(image_path, 'rb').read()
	# label_lines = [line.rstrip() for line
	#                    in tf.gfile.GFile("logs/output_labels.txt")]
	#print(image_path)
	
	main_path=image_path[:(len(image_path)-len(phot.image.name))]
	
	log_path = main_path+"logs\output_labels.txt"
	#print(log_path)
	label_lines = [line.rstrip() for line
	                   in tf.gfile.GFile(log_path)]

	# Unpersists graph from file
	graph_path = main_path + "logs\output_graph.pb"
	#print(graph_path)
	with tf.gfile.FastGFile(graph_path, 'rb') as f:
	    graph_def = tf.GraphDef()
	    graph_def.ParseFromString(f.read())
	    _ = tf.import_graph_def(graph_def, name='')

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


class StockList(APIView):

	def get(self,request):
		stocks = Stock.objects.all() 
		serializer = StockSerializer(stocks, many = True)
		return Response(serializer.data)

		

	def post(self,request):
		serializer = StockSerializer(data=request.data)

		
		if serializer.is_valid():
			serializer.save()
			print("received")

			#console.log(score)
			requ = imageClassify(serializer)
			#requ = json.dumps(requ)

			img_name = serializer.data['id']
			snippet = Stock.objects.get(id= img_name)
			# comment below line to store the posted imageClassify 
			snippet.delete()
			print("response sent")
			return Response(requ, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# def post(self,request):
	# 	Stock.objects.get(pk=request.DELETE['pk']).delete()
	# 	return HttpResponse()

		

