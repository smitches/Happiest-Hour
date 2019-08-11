from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.http import *
from django.views import generic
from .models import *
from .forms import *

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

# @login_required()
def create_bar(request):
	if request.method == 'POST':
		form = CreateBarForm(request.POST)

		if form.is_valid():
			bar = form.save(commit=False)
			bar.manager = request.user
			bar.approved = False
			bar.save()
			return render(request = request,
				  template_name = "hh_app/thanks.html")

	else:
		form = CreateBarForm()

	return render(request, 'hh_app/create.html', {'form': form})

def create_happy_hour(request, bar_id):
	if request.method == 'POST':
		form = CreateHappyHour(request.POST)

		if form.is_valid():
			try:
				bar = Bar.objects.get(id=bar_id)
			except ObjectDoesNotExist:
				pass
			for day in form.cleaned_data['weekdays']:
				hh = form.save(commit=False)
				hh.day_of_week = day
				hh.bar = bar
			return render(request = request,
				  template_name = "hh_app/thanks.html")

	else:
		form = CreateHappyHour()

	return render(request, 'hh_app/create.html', {'form': form})






