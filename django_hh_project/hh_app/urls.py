from django.urls import path
from .views import *

app_name = 'hh_app'

urlpatterns = [
	path('', home, name="hh_home"),
	path('region/', RegionDetail.as_view(), name='hh_region_detail'),
	path('create_bar/', create_bar, name='hh_bar_form'),
	path('created-bar/', created, name='hh_thanks')
]