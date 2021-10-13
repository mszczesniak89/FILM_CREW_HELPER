from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, CustomAuthenticationForm


class Login(LoginView):
    authentication_form = CustomAuthenticationForm
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('main-page')
    template_name = 'registration/login.html'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main-page')
    template_name = 'registration/register.html'
