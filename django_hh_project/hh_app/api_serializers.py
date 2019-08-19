from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','username','first_name','last_name','email']

class BarSerializer(serializers.ModelSerializer):
	manager = UserSerializer()
	class Meta:
		model = Bar
		fields = '__all__'
		read_only_fields = ["manager"]
		depth = 2

class ReviewSerializer(serializers.ModelSerializer):
	reviewer = UserSerializer()
	bar = BarSerializer()
	class Meta:
		model = Reviews
		fields = '__all__'
		read_only_fields = ["reviewer"]
		depth = 2

class HappyHourSerializer(serializers.ModelSerializer):
	bar = BarSerializer()
	class Meta:
		model = HappyHour
		fields = '__all__'
		read_only_fields = ["bar"]
		depth = 2

class RegionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Region
		fields = '__all__'
#		include_when_nested = ['region_name']

#	def get_field_names(self, *args, **kwargs):
#         field_names = super().get_field_names(*args, **kwargs)
#         if self.parent:
#             field_names = [i for i in field_names if i in self.Meta.include_when_nested]
#         return field_names

class FeatureSerializer(serializers.ModelSerializer):
	class Meta:
		model = Feature
		fields = '__all__'
