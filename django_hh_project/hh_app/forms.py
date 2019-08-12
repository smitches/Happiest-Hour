from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CreateBarForm(forms.ModelForm): 

    class Meta: 
        model = Bar
        exclude = ['manager','approved']

'''class CreateBarForm(forms.Form):
    bar_name = forms.CharField(label='Bar Name', max_length=100)
    street_address = forms.CharField(label='Street Address', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=17, validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Phone number must be entered in the format: '+9999999999'.")])
    region = forms.ModelChoiceField(label='Region', queryset=Region.objects.all(), to_field_name="region_name")
    features = forms.ModelMultipleChoiceField(label='Features', required=False, queryset=Feature.objects.all(), to_field_name="feature_title")'''

class CreateHappyHour(forms.ModelForm):
    days = [("M", "Monday"), ("T", "Tuesday"),("W", "Wednesday"),("Th", "Thursday"),("F", "Friday"), ("Sa", "Saturday"), ("Su", "Sunday")]
    weekdays = forms.MultipleChoiceField(label='Days of the Week', choices=days)

    class Meta: 
        model = HappyHour

        exclude = ['day_of_week', 'bar']

class UniqueUserEmailField(forms.EmailField):
    #An EmailField which only is valid if no User has that email.
    def validate(self, value):
        super(forms.EmailField, self).validate(value)
        try:
            User.objects.get(email = value)
            raise forms.ValidationError("Email already exists")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("Email already exists")
        except User.DoesNotExist:
            pass

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required = False, max_length = 30)
    email = UniqueUserEmailField(required = True, label = 'Email address')
    first_name = forms.CharField(required = True, max_length = 30)
    last_name = forms.CharField(required = True, max_length = 30)

	# class Meta:
	# 	model = User
	# 	fields = ['username','email','first_name','last_name','password1','password2'] 

    def __init__(self, *args, **kwargs):
        #Changes the order of fields, and removes the username field.
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['username','email', 'first_name', 'last_name',
                                'password1', 'password2']

    def save(self, commit=True):
        #Saves the email, first_name and last_name properties, after the normal
        #save behavior is complete.
        user = super(UserCreationForm, self).save(commit)
        if user:
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
        return user
 
class UserUpdateForm(forms.ModelForm):
	username = forms.CharField(required = False, max_length = 30)
	email = UniqueUserEmailField(required = True, label = 'Email address')
	first_name = forms.CharField(required = True, max_length = 30)
	last_name = forms.CharField(required = True, max_length = 30)
	class Meta:
		model = User
		fields = ['username','email','first_name','last_name']


DAY_CHOICES = (
        ('M','Monday'),
        ('T','Tuesday'),
        ('W','Wednesday'),
        ('Th','Thursday'),
        ('F','Friday'),
        ('Sa','Saturday'),
        ('Su','Sunday'),
    )

class HHFilterForm(forms.Form):
    day = forms.ChoiceField(choices=DAY_CHOICES, required=False)
    region = forms.ModelChoiceField(required=False ,queryset=Region.objects.all(), to_field_name="region_name")
    #time
    features = forms.ModelMultipleChoiceField(required=False, queryset=Feature.objects.all(), to_field_name="feature_title")
    star_count = forms.IntegerField(label="Min Ave Star Count",max_value = 5, min_value = 0, required=False)
    food = forms.BooleanField(required = False)
    drinks = forms.BooleanField(required = False)
    
