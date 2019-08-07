from django.shortcuts import render
from django.views import generic
from .models import *

# Create your views here.
def home(request):
	if request.method == "GET":
		pass
	elif request.method == "POST":
		pass
	context_dict = {'somekey':'somevalue', 'otherkey':'othervalue'}
	return render(request = request,
				  template_name = "hh_app/home.html",
				  context = context_dict)

class RegionDetail(generic.DetailView):
	model = Region
	template_name = 'hh_app/region_detail.html'