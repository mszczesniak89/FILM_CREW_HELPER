from braces.views import AnonymousRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserPasswordReset, CustomUserChangeForm


class Login(LoginView):
    authentication_form = CustomAuthenticationForm
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('main-page')
    template_name = 'registration/login.html'


class SignUpView(AnonymousRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main-page')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], )
        login(self.request, user)
        return redirect(self.success_url)


class EditUser(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('main-page')
    template_name = 'registration/edit_user.html'

    def get_object(self, queryset=None):
        return self.request.user


class PasswordReset(PasswordResetView):
    form_class = CustomUserPasswordReset
    template_name = 'registration/password_reset_form.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
