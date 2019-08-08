from django.core.validators import RegexValidator
from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Region(models.Model):
	region_name = models.CharField(max_length = 100)
	def __str__(self):
		return str(self.region_name)

class Feature(models.Model):
	feature_title = models.CharField(max_length = 100)
	description = models.CharField(max_length = 100)
	def __str__(self):
		return str(self.feature_title)

class Bar(models.Model):
	bar_name = models.CharField(max_length = 100)
	street_address = models.CharField(max_length = 100)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # va
	manager = models.ForeignKey(User, on_delete = models.CASCADE)
	approved = models.BooleanField(default = False)
	region = models.ForeignKey(Region, on_delete = models.CASCADE)
	features = models.ManyToManyField(Feature, null=True, blank=True)
	def __str__(self):
		return str(self.bar_name) + ' ' + str(self.street_address)

class HappyHour(models.Model):
	day_of_week = models.CharField(max_length = 2)
	start_time = models.TimeField()
	end_time = models.TimeField()
	bar = models.ForeignKey(Bar, on_delete = models.CASCADE)
	drinks = models.BooleanField(default = False)
	food = models.BooleanField(default = False)
	menu_pdf = models.CharField(max_length = 100)
	def __str__(self):
		return str(self.bar.bar_name) + ': ' + str(self.day_of_week)

class Reviews(models.Model):
	reviewer = models.ForeignKey(User, on_delete = models.CASCADE)
	bar = models.ForeignKey(Bar, on_delete = models.CASCADE)
	star_count = models.IntegerField()
	def __str__(self):
		return str(self.reviewer.username) + ': ' + str(self.bar) + ' - ' + str(self.star_count) + ' stars'

