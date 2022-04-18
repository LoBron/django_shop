from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import Http404, request
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from view_breadcrumbs import ListBreadcrumbMixin

from .models import Product, Category
from .forms import RegisterUserForm, LoginUserForm
from .utils import DataMixin

class ProductList(DataMixin, ListView):

    def get_queryset(self):
        return Product.objects.all().order_by('-availability', 'category').select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items())+list(c_def.items()))

class ProductCategoryList(DataMixin, ListView):

    def get_queryset(self):
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Product.objects.filter(category__tree_id=cat.tree_id).select_related('category').order_by('-availability', 'title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - '+cat.name,
                                      cat_selected=cat.id,
                                      childrens=Category.objects.filter(tree_id=cat.tree_id, parent_id__isnull=False))
        return dict(list(context.items())+list(c_def.items()))

class ProductFilterList(DataMixin, ListView):

    def get_queryset(self):

        category_filter = Q()
        category = self.request.GET.getlist("category")
        cat_id = self.request.GET.get("cat_selected", None)
        if len(category) != 0:
            category_filter &= Q(category__slug__in=category)
        elif cat_id and cat_id != '0':
            select_cat = get_object_or_404(Category, id=int(cat_id))
            category_filter &= Q(category__tree_id=select_cat.tree_id)

        price_filter = Q()
        price_min = self.request.GET.get("price_min")
        if len(price_min) == 0:
            price_min = '0' #нужно ддостать число из базы
        price_max = self.request.GET.get("price_max")
        if len(price_max) == 0:
            price_max = '1000000' #нужно ддостать число из базы
        price_filter &= Q(price__gte=int(price_min)) & Q(price__lte=int(price_max))

        availability_filter = Q()
        availability = self.request.GET.get("availability", None)
        if availability:
            availability_filter &= Q(availability=True)

        return Product.objects.filter(category_filter &
                                      price_filter &
                                      availability_filter
                                      ).select_related('category').order_by('-availability', 'title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        path = self.request.get_full_path().split('?')
        c_def = self.get_user_context(title='Каталог-Фильтр товаров',
                                      path=f"{path[-1]}&")
        cat_selected = self.request.GET.get("cat_selected", None)
        if cat_selected and cat_selected != '0':
            cat_selected = int(cat_selected)
            c_def.update(cat_selected=cat_selected)
            cat = get_object_or_404(Category, id=cat_selected)
            c_def['childrens'] = Category.objects.filter(tree_id=cat.tree_id, parent_id__isnull=False)

        return dict(list(context.items())+list(c_def.items()))

class Search(DataMixin, ListView):
    # paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get('s')
        return Product.objects.filter(Q(title__icontains=search) | Q(slug__icontains=search)).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Поиск',
                                      path=f"s={self.request.GET.get('s')}&")
        return dict(list(context.items())+list(c_def.items()))

class ProductDetail(DataMixin, DetailView):
    template_name = 'catalog/product_detail.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['product'].name))
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

