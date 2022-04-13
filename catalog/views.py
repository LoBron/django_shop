from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import Http404, request
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from .models import Product, Category
from .forms import RegisterUserForm, LoginUserForm
from .utils import DataMixin

class ProductList(DataMixin, ListView):

    def get_queryset(self):
        return Product.objects.all().order_by('-availability', 'category')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items())+list(c_def.items()))

class ProductCategoryList(DataMixin, ListView):

    def get_queryset(self):
        # tree_id = Category.objects.filter(slug=self.kwargs['cat_slug']).values_list('tree_id', flat=True)
        # return Product.objects.filter(category__tree_id=tree_id[0]).order_by('-availability', 'title')
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Product.objects.filter(category__tree_id=cat.tree_id).order_by('-availability', 'title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - '+cat.name,
                                      cat_selected=cat.id,
                                      slug=cat.slug,
                                      childrens=Category.objects.filter(tree_id=cat.tree_id, parent_id__isnull=False))
        return dict(list(context.items())+list(c_def.items()))

class ProductFilterList(DataMixin, ListView):

    def get_queryset(self):
        category = self.request.GET.get("category", None)
        price_min = self.request.GET.get("price_min", 0)
        price_max = self.request.GET.get("price_max", 1000000000)
        availability = self.request.GET.get("availability", None)

        filt = []

        # if category:
        #     # cat = Q()
        #     # cat &= Q(category__name__icontains=category)
        #     # filt.append(cat)
        #     filt.append(Q(category__name__icontains=category))
        # if price_min or price_max:
        #     # price = Q()
        #     # price &= Q(price__gte=int(price_1)) & Q(price__lte=int(price_2))
        #     # filt.append(price)
        #     filt.append(Q(price__gte=int(price_min)) & Q(price__lte=int(price_max)))
        # if availability:
        #     if availability == "True":
        #         avail = True
        #     else:
        #         avail = False
        #     # availability = Q()
        #     # availability &= Q(availability=avail)
        #     # filt.append(availability)
        #     filt.append(Q(availability=avail))

        return Product.objects.filter(*filt)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Фильтр товаров')
        # cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        # c_def = self.get_user_context(title=f'Категория - {cat.name} - Фильтр товаров')
        return dict(list(context.items())+list(c_def.items()))

class Search(DataMixin, ListView):
    paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get('s')
        return Product.objects.filter(Q(title__icontains=search) | Q(slug__icontains=search))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Поиск', s=f"s={self.request.GET.get('s')}&")
        return dict(list(context.items())+list(c_def.items()))

class ProductDetail(DataMixin, DetailView):
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

