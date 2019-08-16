from django.test import TestCase

# Create your tests here.


# importing the requests library 
import requests 
import json

# url = 'https://somedomain.com'
# body = {'name': 'Maryja'}
# headers = {'content-type': 'application/json'}

# r = requests.post(url, data=json.dumps(body), headers=headers)
def reviews_req():  
	# defining the api-endpoint  
	API_ENDPOINT = "http://happierhour.appspot.com/api/reviews"
	r = requests.get(url = API_ENDPOINT)
	# extracting response text  
	print(r.text)
	print(dir(r))

def login_req():
	API_ENDPOINT = "http://happierhour.appspot.com/api/rest-auth/login/"
	# data to be sent to api 
	body = {'username':'hh_admin',
			'password':'hh_password'} 
	headers = {'content-type':'application/json'}
	# sending post request and saving response as response object 
	r = requests.post(url = API_ENDPOINT, data = json.dumps(body), headers=headers) 
	file = open('ouput.txt','w')
	file.write(r.text)
	file.close()

def logout_req():
	API_ENDPOINT = "http://happierhour.appspot.com/api/rest-auth/logout/"
	TOKEN = '94e81320f236e75188927f9c8409b0d987f085ba'

	data = {'key':TOKEN}
	body = {
		'media_type':'application/json',
		'content' : data
	}

	headers = {'content-type':'application/json'}
	print(json.dumps(body))
	# sending post request and saving response as response object 
	r = requests.post(url = API_ENDPOINT, data = json.dumps(body), headers=headers) 
	file = open('ouput.txt','w')
	file.write(r.text)
	file.close()

def options_login_req():
	API_ENDPOINT = "http://happierhour.appspot.com/api/rest-auth/login/"
	r = requests.options(url = API_ENDPOINT)
	file = open('ouput.txt','w')
	file.write(r.text)
	file.close()
def options_user_detail_req():
	API_ENDPOINT = "http://127.0.0.1:8000/api/userdetail/"
	r = requests.options(url = API_ENDPOINT)
	file = open('ouput.txt','w')
	file.write(r.text)
	file.close()

def user_detail_req():
	API_ENDPOINT = "http://127.0.0.1:8000/api/rest-auth/login/"
	# data to be sent to api 
	body = {'pk':'1'} 
	headers = {'content-type':'application/json'}
	# sending post request and saving response as response object 
	r = requests.post(url = API_ENDPOINT, data = json.dumps(body), headers=headers) 
	file = open('ouput.txt','w')
	file.write(r.text)
	file.close()

def post_review():
	API_ENDPOINT = "http://127.0.0.1:8000/api/reviews/"
	TOKEN = 'b679929deeb77ce1355c3752005a248e95e8ed5d'
	body = {
        "star_count": 4,
        "review_text": "Making an API Review from python",
        "reviewer": 2,
        "bar": 1
    }
	headers = {'content-type':'application/json','Authorization':'Token '+TOKEN}
	# sending post request and saving response as response object 
	print(headers)
	r = requests.post(url = API_ENDPOINT, data = json.dumps(body), headers=headers) 
	file = open('output.txt','w')
	file.write(str(r.headers))
	file.write(r.text)
	file.close()

def test_auth():
	API_ENDPOINT = "http://127.0.0.1:8000/api/auth_hello/"
	TOKEN = 'b679929deeb77ce1355c3752005a248e95e8ed5d'
	body = {}
	headers = {'Authorization':'Token '+TOKEN}
	r = requests.get(url = API_ENDPOINT, data = json.dumps(body), headers=headers) 
	
	print(str(r.headers))
	print(r.text)
	

# test_auth()	

# print()

# post_review()