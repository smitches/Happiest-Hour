from .models import *
from .forms import *
from django.contrib.auth.models import User

from rest_framework import viewsets, generics, permissions, views, response
from .api_serializers import *
from django.core.exceptions import PermissionDenied

##########################################################################
##########################################################################
############################ PERMISSIONS #################################
##########################################################################
##########################################################################

class IsReviewerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has a `.reviewer` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.manager == request.user

class IsHHManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.bar.manager == request.user


##########################################################################
##########################################################################
################################ Views ###################################
##########################################################################
##########################################################################

#test authentication
class HelloView(views.APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		content = {'message': 'Hello, World!'}
		return response.Response(content)


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class FeatureListView(generics.ListAPIView):
	queryset = Feature.objects.all()
	serializer_class = FeatureSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ReviewsListCreateView(generics.ListCreateAPIView):
	queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	def perform_create(self,serializer):
		serializer.save(reviewer = self.request.user)

class ReviewView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ReviewSerializer
	permission_classes = [IsReviewerOrReadOnly]
	def get_queryset(self):
		return Reviews.objects.filter(id=self.kwargs.get('pk'))

class MyReviewsView(generics.ListAPIView):
	serializer_class = ReviewSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		return Reviews.objects.filter(reviewer__id = self.request.user.id)

class BarReviewsView(generics.ListAPIView):
	serializer_class = ReviewSerializer
	def get_queryset(self):
		bar_id = self.kwargs.get('bar_id')
		return Reviews.objects.filter(bar__id = bar_id)



class BarListView(generics.ListCreateAPIView):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self,serializer):
    	serializer.save(manager = self.request.user)

class BarView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = BarSerializer
	permission_classes = [IsManagerOrReadOnly]
	def get_queryset(self):
		return Bar.objects.filter(id=self.kwargs.get('pk'))

class MyBarsView(generics.ListAPIView):
	serializer_class = BarSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		return Bar.objects.filter(manager__id = self.request.user.id)



class HappyHourListView(generics.ListAPIView):
    queryset = HappyHour.objects.all()
    serializer_class = HappyHourSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HappyHourView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = HappyHourSerializer
	permission_classes = [IsHHManagerOrReadOnly]
	def get_queryset(self):
		return HappyHour.objects.filter(id=self.kwargs.get('pk'))

class MyHappyHoursView(generics.ListAPIView):
	serializer_class = HappyHourSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		return HappyHour.objects.filter(bar__manager__id = self.request.user.id)

class BarHappyHoursView(generics.ListCreateAPIView):
	serializer_class = HappyHourSerializer
	# permission_classes = [IsManagerOrReadOnly]
	def get_queryset(self):
		bar_id = self.kwargs.get('bar_id')
		return HappyHour.objects.filter(bar__id = bar_id)
	def perform_create(self,serializer):
		bar_id = self.kwargs.get('bar_id')
		if self.request.user != Bar.objects.get(id=bar_id).manager:
			raise PermissionDenied
		serializer.save(bar = Bar.objects.get(id=bar_id))

# class BarHappyHourCreateView(generics.CreateAPIView)
# 	serializer_class = HappyHourSerializer

##########################################################################
##########################################################################
################################ NOTES ###################################
##########################################################################
##########################################################################


'''
NONTOKEN:
/GET REVIEWS FOR A BAR LIST VIEW ONLY
/GET REGIONS LIST VIEW ONLY
/GET FEATURES LIST VIEW ONLY
/GET HAPPY HOURS FOR A BAR LIST VIEW ONLY

TOKEN:
/CREATE A REVIEW BY YOU FOR ANY BAR
/CREATE A BAR BY YOU NOT APPROVED YET, DEPENDS ON GET FEATURES AND GET REGIONS
/CREATE A HAPPY HOUR FOR YOUR BAR

?UPDATE A REVIEW BY YOU FOR ANY BAR
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
