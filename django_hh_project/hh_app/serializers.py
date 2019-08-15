from .models import *
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reviews
		fields = '__all__'
