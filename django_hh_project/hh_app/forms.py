from .models import *
from django.forms import ModelForm


class CreateBarForm(ModelForm): 
	class Meta: 
		model = Bar
		exclude = ['manager','approved']


'''class CreateBarForm(forms.Form):
    bar_name = forms.CharField(label='Bar Name', max_length=100)
    street_address = forms.CharField(label='Street Address', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=17, validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Phone number must be entered in the format: '+9999999999'.")])
    region = forms.ModelChoiceField(label='Region', queryset=Region.objects.all(), to_field_name="region_name")
    features = forms.ModelMultipleChoiceField(label='Features', required=False, queryset=Feature.objects.all(), to_field_name="feature_title")'''


class CreateHappyHour(ModelForm):
	class Meta: 
		model = HappyHour
		fields = '__all__'

