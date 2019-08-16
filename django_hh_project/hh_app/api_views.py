from .models import *
from .forms import *
from django.contrib.auth.models import User

from rest_framework import viewsets, generics
from .api_serializers import *


class ReviewsViewSet(viewsets.ModelViewSet):
	queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer
	
class ReviewsListView(generics.ListCreateAPIView):
	queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer
	

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

