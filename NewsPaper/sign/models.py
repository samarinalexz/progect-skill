from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms


class BaseRegisterForms(UserCreationForm):
    email = forms.EmailField(label='Email')
    firs_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2',)


class BaseSignupForm(SignupForm):
    def save(self, request):
        user = super(BaseSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
# Create your models here.
