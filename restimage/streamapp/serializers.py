from rest_framework import serializers
from .models import VideoStream

class VideoStreamSerializer(serializers.ModelSerializer):
	class Meta:
		model = VideoStream
		fields = ('__all__')
