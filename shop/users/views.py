from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (LoginView as Login,
                                       PasswordResetView as PasswordReset,
                                       PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils.translation import gettext_lazy as _

from .forms import *


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        context = {
            'form': RegisterUserForm,
            'title': _('Регистрация')
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.data.get('email')
            password = form.data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            context = {
                'form': form,
                'title': _('Регистрация')
            }
            return render(request, self.template_name, context)


class LoginView(Login):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Авторизация')
        return context


class PasswordResetView(PasswordReset):
    template_name = 'users/password_reset_form.html'
    form_class = PasswordResetUserForm
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Восстановление пароля')
        return context


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = SetPasswordUserForm
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = "catalog/register.html"
#
#     # success_url = reverse_lazy('home')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['logo'] = 'Регистрация'
#         return context
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')
#
#
# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = "catalog/login.html"
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['logo'] = 'Авторизация'
#         return context
#
#     def get_success_url(self):
#         """Функция нужна когда в настройках не прописан LOGIN_REDIRECT_URL"""
#         return reverse_lazy('home')
#
#
# def logout_user(request):
#     logout(request)
#     return redirect('login')
