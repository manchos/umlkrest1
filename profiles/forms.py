from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):



    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'mchs_phone_numb', 'sity_phone_numb')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'mchs_phone_numb', 'sity_phone_numb')
