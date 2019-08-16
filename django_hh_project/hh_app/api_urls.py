from django.urls import path, include
from .api_views import *
from rest_framework import routers


# app_name = 'hh_api'

# router = routers.DefaultRouter()
# router.register('reviews', ReviewsViewSet)

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('reviews/',ReviewsListView.as_view(),name='api_login'),
    path('users/',UserListView.as_view(),name='api_users')
]