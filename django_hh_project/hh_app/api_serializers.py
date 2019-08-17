from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reviews
		fields = '__all__'
		read_only_fields = ["reviewer"]

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','username','first_name','last_name','email']

class HappyHourSerializer(serializers.ModelSerializer):
	class Meta:
		model = HappyHour
		fields = '__all__'
		read_only_fields = ["bar"]

class BarSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bar
		fields = '__all__'
		read_only_fields = ["manager"]

class RegionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Region
		fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
	class Meta:
		model = Feature
		fields = '__all__'

# class HappyHourInfoSerializer(serializers.Serializer):
# 	day = serializers.CharField(max_length=2,required=False)
# 	region_id = serializers.IntegerField(required=False)
# 	feature_ids = serializers.IntegerField(required=False)
# 	star_count = serializers.FloatField(required=False)
# 	drinks = serializers.BooleanField(required=False)
# 	food = serializers.BooleanField(required=False)
