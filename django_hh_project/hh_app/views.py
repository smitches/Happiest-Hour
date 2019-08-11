from django.shortcuts import render
from django.views import generic
from .models import *

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
			return redirect(reverse('hh_app:hh_home'))
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

	def test_func(self):
		bar_id = self.kwargs.get('pk')
		bar = Bar.objects.get(id=bar_id)
		return self.request.user == bar.manager

class HHUpdate(UserPassesTestMixin,generic.UpdateView):
	#only bar manager can update
	model = HappyHour
	template_name = 'hh_app/hh_update.html'
	fields = ['start_time','end_time','drinks','food','menu_pdf']

	def test_func(self):
		hh_id = self.kwargs.get('pk')
		hh = HappyHour.objects.get(id=hh_id)
		return self.request.user == hh.bar.manager

class ReviewUpdate(UserPassesTestMixin, generic.UpdateView):
	model = Reviews
	template_name = 'hh_app/review_update.html'
	fields = ['star_count','review_text']
	success_url = reverse_lazy('hh_app:hh_home')
	def test_func(self): #The test to see if user is creator of review
		review_id = self.kwargs.get('pk')
		review = Reviews.objects.get(id=review_id)
		return review.reviewer == self.request.user

class ReviewCreate(LoginRequiredMixin,generic.CreateView):
	model = Reviews
	fields = ['bar','star_count','review_text']
	template_name = 'hh_app/review_create.html'
	def form_valid(self,form):
		form.instance.reviewer = self.request.user
		return super().form_valid(form)
