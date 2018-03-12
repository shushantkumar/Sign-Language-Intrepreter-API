from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stock
		#fields = ('ticker','volume')		#for specific
		fields = ('__all__')


