from django.urls import path, include
from .api_views import *
from rest_framework import routers


# app_name = 'hh_api'

# router = routers.DefaultRouter()
# router.register('reviews', ReviewsViewSet)

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('reviews/',ReviewsListCreateView.as_view()),
    path('users/',UserListView.as_view()),
    path('bars/',BarListView.as_view()),
    path('features/',FeatureListView.as_view()),
    path('regions/',RegionListView.as_view()),
    path('happyhours/',HappyHourListView.as_view()),

    path('bar/<int:bar_id>/reviews/',BarReviewsView.as_view()),
    path('bar/<int:bar_id>/happyhours/',BarHappyHoursView.as_view()),
    # path('bar/<int:bar_id>/happyhours/create/',BarHappyHourCreateView.as_view()),

    path('myreviews/',MyReviewsView.as_view()),
    path('mybars/',MyBarsView.as_view()),
    path('myhappyhours/',MyHappyHoursView.as_view()),

    path('userdetail/<int:pk>/',UserDetailView.as_view()),
    path('review/<int:pk>/',ReviewView.as_view()),
    path('bar/<int:pk>/',BarView.as_view()),
    path('happyhour/<int:pk>/',HappyHourView.as_view()),

    path('auth_hello/',HelloView.as_view()),
]