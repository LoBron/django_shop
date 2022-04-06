from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from .models import Product, Category
from .forms import RegisterUserForm, LoginUserForm
from .utils import DataMixin

# def show_catalog(request):
#     products = Product.objects.all()
#     categoryes = Category.objects.all().order_by('name')
#     data = {
#         'products': products,
#         'categoryes': categoryes,
#         'title': 'Каталог',
#         'logo': 'Категории',
#     }
#     return render(request, 'catalog/product_list.html', data)

class ProductList(DataMixin, ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('-availability', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items())+list(c_def.items()))


# def show_category(request, cat_slug):
#     # cat = get_object_or_404(Category, slug=cat_slug)
#     products = Product.objects.filter(category__slug=cat_slug)
#     # name_cat = products.get()
#     # if len(products) == 0:
#     #     raise Http404()
#     data = {
#         'products': products,
#         'title': '---//---',
#         'logo': '---//---',
#     }
#     return render(request, 'catalog/catalog_category.html', data)

class ProductCategoryList(DataMixin, ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['cat_slug']).order_by('-availability', 'title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - '+cat.name,
                                      cat_selected=cat.id)
        return dict(list(context.items())+list(c_def.items()))

class Search(DataMixin, ListView):
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        search = self.request.GET.get('s')
        return Product.objects.filter(Q(title__icontains=search) | Q(slug__icontains=search))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Поиск', s=f"s={self.request.GET.get('s')}&")
        return dict(list(context.items())+list(c_def.items()))

class ProductDetail(DataMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['product'].title))
        return dict(list(context.items())+list(c_def.items()))

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

