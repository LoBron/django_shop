from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView

from catalog.models import Product, Category

from catalog.forms import RegisterUserForm, LoginUserForm




def show_catalog(request):
    products = Product.objects.all()
    categoryes = Category.objects.all().order_by('name')
    data = {
        'products': products,
        'categoryes': categoryes,
        'title': 'Каталог',
        'logo': 'Категории',
    }
    return render(request, 'catalog/catalog_home.html', data)

class ProductList(ListView):
    model = Product
    template_name = 'catalog/catalog_home.html'
    context_object_name = 'products'
    data = {
        'categoryes': categoryes,
        'title': 'Каталог',
        'logo': 'Категории',
    }

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        for i in data:

        context['now'] = timezone.now()
        return context

def show_category(request, cat_slug):
    # cat = get_object_or_404(Category, slug=cat_slug)
    products = Product.objects.filter(category__slug=cat_slug)
    # name_cat = products.get()
    # if len(products) == 0:
    #     raise Http404()
    data = {
        'products': products,
        'title': '---//---',
        'logo': '---//---',
    }
    return render(request, 'catalog/catalog_category.html', data)

class ProductDetail(DetailView):
    model = Product
    template_name = 'catalog/catalog_category_product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "catalog/register.html"
    # success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = 'Регистрация'
        return context
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "catalog/login.html"

    def get_context_data(self, *, object_list=None,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = 'Авторизация'
        return context
    def get_success_url(self):
        """Функция нужна когда в настройках не прописан LOGIN_REDIRECT_URL"""
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')