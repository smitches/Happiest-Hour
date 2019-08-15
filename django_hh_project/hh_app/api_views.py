from .models import *

from rest_framework import viewsets
from .serializers import *

class ReviewsViewSet(viewsets.ModelViewSet):
	queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer
