from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, \
    ReadOnlyPasswordHashField
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
        fields = ['username', 'password1', 'password2', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username...'}),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail....'}),

        }


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="Password", widget=forms.HiddenInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')


class CustomUserPasswordReset(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

    class Meta:
        model = CustomUser
        fields = ['email', ]










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

