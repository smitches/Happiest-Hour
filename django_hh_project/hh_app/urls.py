from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'hh_app'

urlpatterns = [
	path('upload/',upload_form,name='upload_form'),
	path('uploader/',uploader,name='uploader'),
	path('look/<file_name>/',look,name='look'),

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
	path('allbars/', display_all_bars, name='allbars'),
	path('mybars/', display_bars, name='mybars'),
	path('bars/<int:bar_id>/happy_hours', display_bars_happyhours, name='bar_hhs'),
	path('bars/<int:bar_id>/reviews', display_bars_reviews, name='bar_reviews'),
	path('reviews/history/',MyReviewsDisplay.as_view(), name='my_reviews'),
	path('happy_hours/<int:pk>/delete', HappyHourDelete.as_view(), name='hh_delete'),
	path('bars/<int:pk>/delete', BarDelete.as_view(), name='bar_delete'),
	path('reviews/<int:pk>/delete', ReviewDelete.as_view(), name='review_delete'),
	path('info/', project_info, name='project_info'),
	path('about/', project_about, name='project_about')
]