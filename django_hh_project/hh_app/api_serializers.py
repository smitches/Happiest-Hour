from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reviews
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email']
