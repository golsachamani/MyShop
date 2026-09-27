from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, TemplateView, View, base
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import logout
from .forms import ChangeForm, CreationForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

User = get_user_model()


class Register(CreateView):
    form_class = CreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")


class UserLogin(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogout(base.View):
    def get(self, request):
        logout(request)
        return redirect("login")

    def post(self, request):
        logout(request)
        return redirect("login")


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangeForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("password_change_done")


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"
