from django.urls import path, include
from .api_views import *
from rest_framework import routers


# app_name = 'hh_api'

# router = routers.DefaultRouter()
# router.register('reviews', ReviewsViewSet)

urlpatterns = [
	#Login, Logout, Register
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    #GET only, with exception of POSTing a Review
    path('reviews/',ReviewsListView.as_view()),
    path('users/',UserListView.as_view()),
    path('bars/',BarListView.as_view()),
    path('features/',FeatureListView.as_view()),
    path('regions/',RegionListView.as_view()),
    path('happyhours/',HappyHourListView.as_view()),

    #GET or POST when authenticated
	path('reviews/create/',ReviewsListCreateView.as_view()),
    path('bars/create/',BarListCreateView.as_view()),
    path('bar/<int:bar_id>/happyhours/create',BarHappyHoursCreateView.as_view()),

    path('bar/<int:pk>/delete/',deleteBar),
    path('happy_hour/<int:pk>/delete/',deleteHappyHour),
    path('review/<int:pk>/delete/',deleteReview),

    #GET only
    path('bar/<int:bar_id>/reviews/',BarReviewsView.as_view()),
    #GET list or POST a new happy hour (checks to make sure you are Manager first)
    path('bar/<int:bar_id>/happyhours/',BarHappyHoursView.as_view()),

    #GET only, rely on token to get the affiliated values
    path('myreviews/',MyReviewsView.as_view()),
    path('mybars/',MyBarsView.as_view()),
    path('myhappyhours/',MyHappyHoursView.as_view()),

    #GET
    path('userdetail/<int:pk>/',UserDetailView.as_view()),
    path('whoami/',UserLoggedInView.as_view()),

    #GET, PUT, PATCH, DELETE. Checks Permissions first.
    path('review/<int:pk>/',ReviewView.as_view()),
    path('bar/<int:pk>/',BarView.as_view()),
    path('happyhour/<int:pk>/',HappyHourView.as_view()),

    #POST. body utilizing all filters should have following schema: 
    # '''
    # {
    # 	'day':'M',
    # 	'region_id':1,
    # 	'feature_ids': [
    # 		{'feature_id':1},
    # 		{'feature_id':2}
    # 	],
    # 	'star_count':3,
    # 	'drinks':1,			OR 'drinks':True		 OR 'drinks':'True'
    # 	'food':0 			OR 'food':False 		NOT 'food':'False'
    # }
    # '''
    path('happyhours/search/',happyhour_search),

    #Test your token
    path('auth_hello/',HelloView.as_view()),
]