from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'hh_app'

urlpatterns = [
	path('', home, name="home"),
	path('create_bar/', create_bar, name='bar_form'),
	path('create_happy_hour/<int:bar_id>/', create_happy_hour, name='hh_form'),
	path('region/<int:pk>/', RegionDetail.as_view(), name='region_detail'),
	path('reviews/<int:pk>/update/',ReviewUpdate.as_view(), name='update_review'),
	path('reviews/create/',ReviewCreate.as_view(),name='create_review'),
	path('bars/<int:pk>/update/',BarUpdate.as_view(), name='update_bar'),
	path('happy_hours/<int:pk>/update/',HHUpdate.as_view(), name='update_hh'),
	path('search/', search_hhs ,name='search'),
	path('register/',register,name='register'),
	path('account/',account, name='account'),
	path('logout/', auth_views.LogoutView.as_view(template_name='hh_app/logout.html'), name='logout'),
	path('login/', auth_views.LoginView.as_view(template_name='hh_app/login.html'), name='login'),
	path('mybars/', display_bars, name='mybars'),
	path('bars/<int:bar_id>/happy_hours', display_bars_happyhours, name='bar_hhs'),
	path('reviews/history/',MyReviewsDisplay.as_view(), name='my_reviews')
]