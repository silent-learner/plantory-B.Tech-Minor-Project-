
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import PostMessage



class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2','first_name','last_name']


class CreatePostForm(ModelForm):
	class Meta:
		model = PostMessage
		fields = '__all__'
		exclude = ['user']