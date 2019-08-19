from .models import *
from .forms import *
from django.contrib.auth.models import User

from rest_framework import viewsets, generics, permissions, views, response
from rest_framework.decorators import api_view
from .api_serializers import *
from django.core.exceptions import PermissionDenied

from django.db.models import Q, Avg
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

class UserLoggedInView(generics.ListAPIView):
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		return User.objects.filter(id = self.request.user.id)


class ReviewsListCreateView(generics.ListCreateAPIView):
	queryset = Reviews.objects.all()
	serializer_class = ReviewCreateSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	def perform_create(self,serializer):
		serializer.save(reviewer = self.request.user)

class ReviewsListView(generics.ListAPIView):
	queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer

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



class BarListCreateView(generics.ListCreateAPIView):
    queryset = Bar.objects.all()
    serializer_class = BarCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self,serializer):
    	serializer.save(manager = self.request.user)

class BarListView(generics.ListAPIView):
	queryset = Bar.objects.all()
	serializer_class = BarSerializer

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

class BarHappyHoursView(generics.ListAPIView):
	serializer_class = HappyHourSerializer
	# permission_classes = [IsManagerOrReadOnly]
	def get_queryset(self):
		bar_id = self.kwargs.get('bar_id')
		return HappyHour.objects.filter(bar__id = bar_id)

class BarHappyHoursCreateView(generics.ListCreateAPIView):
	serializer_class = HappyHourCreateSerializer
	# permission_classes = [IsManagerOrReadOnly]
	def get_queryset(self):
		bar_id = self.kwargs.get('bar_id')
		return HappyHour.objects.filter(bar__id = bar_id)
	def perform_create(self,serializer):
		bar_id = self.kwargs.get('bar_id')
		if self.request.user != Bar.objects.get(id=bar_id).manager:
			raise PermissionDenied
		serializer.save(bar = Bar.objects.get(id=bar_id))


@api_view(['GET','POST'])
def happyhour_search(request):
	if request.method == 'POST':
		if 'day' in request.data.keys():
			day = request.data['day']
		else:
			day = ""

		if 'region_id' in request.data.keys():
			region_id = int(request.data['region_id'])
		else:
			region_id = 0

		if 'feature_ids' in request.data.keys():
			feature_ids = list(request.data['feature_ids'])
		else:
			feature_ids = []
		
		if 'star_count' in request.data.keys():
			star_count = float(request.data['star_count'])
		else:
			star_count = 0
		
		if 'drinks' in request.data.keys():
			drinks = bool(request.data['drinks'])
		else:
			drinks = False
		
		if 'food' in request.data.keys():
			food = bool(request.data['food'])
		else:
			food = False


		if day:
			qualifying_hhs = HappyHour.objects.filter(day_of_week = day)
		else:
			qualifying_hhs = HappyHour.objects


		if drinks:
			qualifying_hhs = qualifying_hhs.filter(drinks=True)
		if food:
			qualifying_hhs = qualifying_hhs.filter(food=True)


		qualifying_bars = Bar.objects.filter(approved=True)
		if star_count:
			qualifying_bars = Bar.objects.annotate(ave_stars = Avg('reviews__star_count')).filter(ave_stars__gte = star_count)
		if region_id:
			qualifying_bars = Bar.objects.filter(region__id = region_id)
		for feature_dict in feature_ids:
			feature_id = int(feature_dict['feature_id'])
			f_bars = (Feature.objects.get(id = feature_id)).bar_set.all()
			qualifying_bars = qualifying_bars & f_bars

		final_hhs = qualifying_hhs.filter(Q(bar__in=list(qualifying_bars))).all()

		hh_serializer = HappyHourSerializer(final_hhs,many=True)

		return response.Response(hh_serializer.data)
	return response.Response({"hello":"world"})

# class HappyHourSearchView(views.APIView):
# 	# http_method_names = ['GET','POST','OPTIONS','HEAD']
# 	def get(self,request):
# 		hhs = HappyHour.objects.all()
# 		hh_serializer = HappyHourSerializer(hhs, many=True)
# 		return response.Response(hh_serializer.data)
# 	def post(self,request):
# 		print(request.kwargs or None)
# 		print(self.kwargs or None)
# 		hhs = HappyHour.objects.all()
# 		hh_serializer = HappyHourSerializer(hhs, many=True)
# 		return response.Response(hh_serializer.data)

'''
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
