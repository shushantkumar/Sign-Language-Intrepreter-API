from rest_framework import serializers
from .models import VideoSign

class VideoSignSerializer(serializers.ModelSerializer):
	class Meta:
		model = VideoSign
		#fields = ('ticker','volume')		#for specific
		fields = ('__all__')
