from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username...'}))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password...'}))


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password...'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Re-enter password...'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username...',
            })
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', )










# class CreateUserForm(UserCreationForm):
#     password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
#         attrs={'class': 'form-control', 'placeholder': 'Password...'}))
#     password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
#         attrs={'class': 'form-control', 'placeholder': 'Re-enter password...'}))
#
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password1', 'password2']
#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Username...',
#             }),
#
#
#
#         }

