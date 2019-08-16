from .models import *
from .forms import *
from django.contrib.auth.models import User

from rest_framework import viewsets, generics, permissions, views, response
from .api_serializers import *

class HelloView(views.APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		content = {'message': 'Hello, World!'}
		return response.Response(content)

class ReviewsListCreateView(generics.ListCreateAPIView):
	queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BarListView(generics.ListAPIView):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer

class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    # http_method_names = ['get']

class HappyHourListView(generics.ListAPIView):
    queryset = HappyHour.objects.all()
    serializer_class = HappyHourSerializer

class FeatureListView(generics.ListAPIView):
	queryset = Feature.objects.all()
	serializer_class = FeatureSerializer


class BarReviewsView(generics.ListAPIView):
	# TODO ONLY ALLOW TOKENED USERS TO POST/CREATE A BAR'S REVIEW
	serializer_class = ReviewSerializer
	def get_queryset(self):
		bar_id = self.kwargs.get('bar_id')
		return Reviews.objects.filter(bar__id = bar_id)

# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class BarListView(generics.ListAPIView):
#     queryset = Bar.objects.all()
#     serializer_class = BarSerializer

# class RegionListView(generics.ListAPIView):
#     queryset = Region.objects.all()
#     serializer_class = RegionSerializer
#     # http_method_names = ['get']

# class HappyHourListView(generics.ListAPIView):
#     queryset = HappyHour.objects.all()
#     serializer_class = HappyHourSerializer

# class FeatureListView(generics.ListAPIView):
# 	queryset = Feature.objects.all()
# 	serializer_class = FeatureSerializer


'''
NONTOKEN:
GET REVIEWS FOR A BAR LIST VIEW ONLY
GET REGIONS LIST VIEW ONLY
GET FEATURES LIST VIEW ONLY
GET HAPPY HOURS FOR A BAR LIST VIEW ONLY

TOKEN:
CREATE A REVIEW BY YOU FOR ANY BAR
CREATE A BAR BY YOU NOT APPROVED YET, DEPENDS ON GET FEATURES AND GET REGIONS
CREATE A HAPPY HOUR FOR YOUR BAR

UPDATE A REVIEW BY YOU FOR ANY BAR
UPDATE A BAR BY YOU, ITS FEATURES, ITS PHONE BLAH
UPDATE A HAPPY HOUR FOR YOUR BAR

DELETE A REVIEW BY YOU FOR ANY BAR
DELETE A BAR BY YOU, ITS FEATURES, ITS PHONE BLAH
DELETE A HAPPY HOUR FOR YOUR BAR

GET REVIEWS BY YOU (TOKEN)
GET BARS BY YOU (TOKEN) mANGER
GET HAPPY HOURS FOR YOUR BAR MANAGER (TOKEN)

'''
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
