from .models import *
from .forms import *

from rest_framework import viewsets
from .serializers import *

#for files
from django.shortcuts import *
from django.http import *
from google.cloud import storage
from google.cloud.storage import Blob
from werkzeug.utils import secure_filename
import io
import requests


class ReviewsViewSet(viewsets.ModelViewSet):
	queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer


def uploader(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():

			file = request.FILES['file']
			bucket_name = "menus_happierhour"
			client = storage.Client()
			bucket = client.get_bucket(bucket_name)
			blob = bucket.blob(secure_filename(file.name))
			try:
				blob.upload_from_file(file.file)
				return JsonResponse({"success": True})
			except Exception as e:
				logging.exception(e)
				return JsonResponse({"success": False})
	return JsonResponse({'success':False})


def upload_form(request):
	return render(request=request,template_name='files/upload.html', context={'form':UploadFileForm()})
def look(request,file_name):
	# try:
	# Reformat the filename using the bucket name fetched above
		bucket_name = "menus_happierhour"
		client = storage.Client()
		bucket = client.get_bucket(bucket_name)
		blob = bucket.blob(secure_filename(file_name))
		data = blob.download_as_string()	
		extension = secure_filename(file_name).rsplit('.', 1)[1]
		if extension == "png":
			return FileResponse(io.BytesIO(data),content_type='image/png')

		elif extension == 'pdf':
			return FileResponse(io.BytesIO(data),content_type='application/pdf')
		else:
			return FileResponse(io.BytesIO(data))
	# except Exception as e: 
	# 	return JsonResponse({'error': 'Could not find file {}'.format(file_name)})
	
