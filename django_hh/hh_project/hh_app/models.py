from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Region(models.Model):
	region_name = models.CharField(max_length = 100)
	def __str__(self):
		return str(self.region_name)

class Bar(models.Model):
	bar_name = models.CharField(max_length = 100)
	street_address = models.CharField(max_length = 100)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # va
	#manager
	approved = models.BooleanField(default = False)
	region = models.ForeignKey(Region, on_delete = models.CASCADE)
