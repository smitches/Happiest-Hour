from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.http import *
from django.views import generic
from .models import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .forms import UserRegisterForm


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


def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			#TODO: add messages to base template
			messages.success(request, f'Your account has been created {username}!')
			#TODO: log user in
			return redirect(reverse('hh_app:login'))
	else:
		form = UserRegisterForm()
	return render(request, 'hh_app/register.html', {"form":form})

@login_required
def account(request):
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		if u_form.is_valid():
			u_form.save()
			username=form.cleaned_data.get('username')
			messages.success(request, f'{username}, your account has been updated!')
			return redirect(reverse('hh_app:home'))
	else:
		u_form = UserUpdateForm(instance=request.user)
	context = {
		'u_form': u_form
	}
	return render(request, 'users/profile.html', context)

class RegionDetail(generic.DetailView):
	model = Region
	template_name = 'hh_app/region_detail.html'

class RegionUpdate():
	pass #Not Necessary: will only be edited by admin in dashboard

class FeatureUpdate():
	pass #Not Necessary. Changing features will only happen by admin.
	#NOTE: bar managers can change bar features in bar edit

class BarUpdate(UserPassesTestMixin, generic.UpdateView):
	#only manager can update
	model = Bar
	template_name = 'hh_app/bar_update.html'
	fields = ['bar_name','street_address','phone_number','region','features']
	success_url = reverse_lazy('hh_app:home')
	def test_func(self):
		bar_id = self.kwargs.get('pk')
		bar = Bar.objects.get(id=bar_id)
		return self.request.user == bar.manager

class HHUpdate(UserPassesTestMixin,generic.UpdateView):
	#only bar manager can update
	model = HappyHour
	template_name = 'hh_app/update_hh.html'
	fields = ['start_time','end_time','drinks','food','menu_pdf']
	success_url = reverse_lazy('hh_app:home')
	def test_func(self):
		hh_id = self.kwargs.get('pk')
		hh = HappyHour.objects.get(id=hh_id)
		return self.request.user == hh.bar.manager

class ReviewUpdate(UserPassesTestMixin, generic.UpdateView):
	model = Reviews
	template_name = 'hh_app/review_update.html'
	fields = ['star_count','review_text']
	success_url = reverse_lazy('hh_app:home')
	def test_func(self): #The test to see if user is creator of review
		review_id = self.kwargs.get('pk')
		review = Reviews.objects.get(id=review_id)
		return review.reviewer == self.request.user

class ReviewCreate(LoginRequiredMixin,generic.CreateView):
	model = Reviews
	fields = ['bar','star_count','review_text']
	template_name = 'hh_app/review_create.html'
	success_url = reverse_lazy('hh_app:home')
	def form_valid(self,form):
		form.instance.reviewer = self.request.user
		return super().form_valid(form)


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
				#TODO: don;t you need to commit it now?
			return render(request = request,
				  template_name = "hh_app/thanks.html")

	else:
		form = CreateHappyHour()

	return render(request, 'hh_app/create.html', {'form': form})

def search_hhs(request):
	if request.method == 'POST':
		form = HHFilterForm(request.POST)
		if form.is_valid():
			a = form.cleaned_data['day']
			b = form.cleaned_data['day']
			c = form.cleaned_data['day']
			d = form.cleaned_data['day']
			raise Exception
	else:
		form = HHFilterForm()
	return render(request,'hh_app/filter.html',{'form':form})
