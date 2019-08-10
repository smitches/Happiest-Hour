from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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
		bar = Bar(manager=request.user, approved=False)
		form = CreateBarForm(request.POST, instance=bar)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/thanks/')

	else:
		form = CreateBarForm()

	return render(request, 'hh_app/create_bar.html', {'form': form})

def created(request):
	return render(request, 'hh_app/thanks.html')






