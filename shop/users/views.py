from typing import Optional

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (LoginView as Login,
                                       PasswordResetView as PasswordReset,
                                       PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView)
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.views.generic import TemplateView

from .forms import *
from .utils import send_email_to_verify

UserModel = get_user_model()


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
            send_email_to_verify(request, user, use_https=False)
            # login(request, user)
            return redirect('confirm_email')
        else:
            context = {
                'form': form,
                'title': _('Регистрация')
            }
            return render(request, self.template_name, context)


class LoginView(Login):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    # def form_valid(self, form):
    #     user = form.get_user()
    #     if user.email_verify:
    #         login(self.request, user)
    #         return redirect('home')
    #     else:
    #         send_email_to_verify(self.request, user, use_https=False)
    #         return redirect('confirm_email')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Авторизация')
        return context


class LoginAjaxView(View):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return JsonResponse(
                    data={'status': 201},
                    status=200
                )
            return JsonResponse(
                data={'status': 400, 'error': 'Your data is not valid.'},
                status=200
            )
        return JsonResponse(
            data={'status': 400, 'error': 'Enter your email and password.'},
            status=200
        )
        # return {'status': True}


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


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64) -> Optional[User]:
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

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
