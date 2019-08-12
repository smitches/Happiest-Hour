from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.http import *
from django.views import generic
from .models import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
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
			# messages.success(request, f'Your account has been created {username}!')
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
	success_url = reverse_lazy('hh_app:mybars')
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
		self.bar = hh.bar
		return self.request.user == hh.bar.manager
	def get_success_url(self):
		return reverse('hh_app:bar_hhs', kwargs={'bar_id': self.bar.id})

class ReviewUpdate(UserPassesTestMixin, generic.UpdateView):
	model = Reviews
	template_name = 'hh_app/review_update.html'
	fields = ['star_count','review_text']
	success_url = reverse_lazy('hh_app:my_reviews')
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

class HappyHourDelete(UserPassesTestMixin, generic.DeleteView):
	model = HappyHour
	template_name = 'hh_app/hh_delete.html'
	def test_func(self):
		self.bar = HappyHour.objects.get(id = self.kwargs.get('pk')).bar
		return self.bar.manager==self.request.user
	def get_success_url(self):
		return reverse('hh_app:bar_hhs', kwargs={'bar_id': self.bar.id})

class BarDelete(UserPassesTestMixin, generic.DeleteView):
	model = Bar
	template_name = 'hh_app/bar_delete.html'
	def test_func(self):
		bar = Bar.objects.get(id = self.kwargs.get('pk'))
		return bar.manager==self.request.user
	def get_success_url(self):
		return reverse('hh_app:mybars')


@login_required
def create_bar(request):
	if request.method == 'POST':
		form = CreateBarForm(request.POST)

		if form.is_valid():
			bar = form.save(commit=False)
			bar.manager = request.user
			bar.approved = False
			bar.save()
			return redirect(reverse('hh_app:mybars'))

	else:
		form = CreateBarForm()

	return render(request, 'hh_app/bar_create.html', {'form': form})

@login_required
def create_happy_hour(request, bar_id):
	
	bar = Bar.objects.get(id=bar_id)
	
	if bar.manager != request.user:
		return HttpResponseForbidden()

	if request.method == 'POST':
		form = CreateHappyHour(request.POST)

		if form.is_valid():
			for day in form.cleaned_data['weekdays']:
				hh = HappyHour(day_of_week=day, bar = bar)
				form = CreateHappyHour(request.POST, instance=hh)
				form.save()

			return redirect(reverse('hh_app:bar_hhs', kwargs={'bar_id': bar.id}))

	else:
		form = CreateHappyHour()

	return render(request, 'hh_app/hh_create.html', {'form': form})

def search_hhs(request):
	if request.method == 'POST':
		form = HHFilterForm(request.POST)
		if form.is_valid():
			day = form.cleaned_data['day']
			#time
			region = form.cleaned_data['region']
			features = form.cleaned_data['features']
			star_count = form.cleaned_data['star_count']
			drinks = form.cleaned_data['drinks']
			food = form.cleaned_data['food']

			qualifying_hhs = HappyHour.objects.filter(day_of_week = day)
			if drinks:
				qualifying_hhs = qualifying_hhs.filter(drinks=True)
			if food:
				qualifying_hhs = qualifying_hhs.filter(food=True)

			qualifying_bars = Bar.objects.filter(approved=True)
			if star_count:
				qualifying_bars = Bar.objects.annotate(ave_stars = Avg('reviews__star_count')).filter(ave_stars__gte = star_count)
			if region:
				qualifying_bars = Bar.objects.filter(region = region)
			for feature in features:
				f_bars = (Feature.objects.get(id = feature.id)).bar_set.all()
				qualifying_bars = qualifying_bars & f_bars

			final_hhs = list(qualifying_hhs.filter(Q(bar__in=list(qualifying_bars))).all())

			return render(request,'hh_app/filtered_hhs.html',{'hh_list':final_hhs})

	else:
		form = HHFilterForm()
	return render(request,'hh_app/filter.html',{'form':form})

'''
LOOKING AT EACH HAPPY HOUR.
WHAT IS THE HH'S BAR.
WHAT ARE THE HH BAR'S FEATURES
DOES A BAR HAVE EVERY ONE OF THE FEATURES?
WHICH HHS BELONG TO THOSE BARS
'''




class MyReviewsDisplay(LoginRequiredMixin,generic.ListView):
	model = Reviews
	template_name = 'hh_app/my_reviews_display.html'
	def get_queryset(self):
		return self.request.user.reviews_set.all()

def display_bars(request):
	return render(request, 'hh_app/display_bars.html', {'bars': request.user.bar_set.all()})

def display_bars_happyhours(request, bar_id):
	bar_obj = Bar.objects.get(id=bar_id)
	return render(request, 'hh_app/display_hhs.html', {'bar': bar_obj, 'hhs': bar_obj.happyhour_set.all().order_by('day_of_week')})
