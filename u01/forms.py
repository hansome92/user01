__author__ = 'administrator'

from django import forms
from models import *

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    #input_formats=settings.DATE_INPUT_FORMATS
    birthday = forms.DateField()
    class Meta:
        model = UserProfile
        fields = ('birthday', 'random')