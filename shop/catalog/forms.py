from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from shop.catalog import Product, Category


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    #     # widgets = {
    #     #     'email': forms.TextInput(attrs={c})
    #     # }

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'id': "floatingInput"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'password1', 'password2')

# class AddDataCategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'slug', 'price', 'availability', 'amount', 'main_photo']

class AddDataProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', "description", 'price', 'availability', 'amount', 'main_photo']

