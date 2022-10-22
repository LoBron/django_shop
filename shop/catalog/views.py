from typing import Optional, List

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from cart.forms import CartAddProductForm
from .models import Product, Category, Property, PropertyValue
from .utils import DataMixin, num_to_word


class ProductList(DataMixin, ListView):

    def get_queryset(self):
        return Product.objects.all().order_by('-availability', 'category').select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class ProductCategoryList(DataMixin, ListView):
    products: QuerySet

    def get_queryset(self):
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        childrens = cat.get_children()
        slugs = [cat.slug]
        if childrens:
            for children in childrens:
                slugs.append(children.slug)
        products = (Product.objects
                    .filter(category__slug__in=slugs)
                    .select_related('category')
                    .order_by('-availability', 'name'))
        self.products = products
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        parent_selected_cat = get_object_or_404(Category, id=selected_cat.parent_id)
        childrens = selected_cat.get_children()
        id_list = []
        if childrens:
            for child in childrens:
                id_list.append(child.id)
        else:
            id_list.append(selected_cat.id)

        # prod = Product.objects.filter(propertyvalue__property=513)
        # print(prod)
        # for i in prod:
        #     print(i)

        # cat_0 = get_object_or_404(Category, tree_id=selected_cat.tree_id, parent_id__isnull=True)
        properties = (Property.objects
                      .prefetch_related('products')
                      .filter(products__category__in=id_list)
                      .order_by('id', 'name').distinct('id'))
        # for prop in properties:
        #     print(prop.name)
        query = {}
        n = 2
        for pr in properties:
            values = (PropertyValue.objects
                      .select_related('product')
                      .filter(property=pr.id, product__category__in=id_list)
                      .order_by('value')
                      .distinct('value')
                      .values('id', 'value'))
            query[pr.name] = {'values': values, 'num_word': num_to_word(n), 'property_id': pr.id}
            n += 1
        # for v in values:
        #     print(v.property.name, ' - ', v.product.name, ' - ', v.value)

        if selected_cat.level == 1:
            name = selected_cat.name
        elif selected_cat.level == 2:
            name = parent_selected_cat.name
        # ch = Category.objects.filter(parent_id=cat_0.id)
        c_def = self.get_user_context(title='Категория - ' + selected_cat.name,
                                      logo1=name,
                                      # properties=properties,
                                      # values=values,
                                      cat_selected=selected_cat.id,
                                      cat_slug=self.kwargs['cat_slug'],
                                      # ch=ch,
                                      properties=query,
                                      childrens=selected_cat.get_children() if selected_cat.level == 1
                                      else parent_selected_cat.get_children(),
                                      parent=get_object_or_404(Category, id=selected_cat.parent_id))
        return dict(list(context.items()) + list(c_def.items()))


def product_list(request):
    p = None
    return render(request, 'polls/detail.html', {'poll': p})


class ProductFilterList(DataMixin, ListView):

    @staticmethod
    def get_category_filter(cat_id: Optional[str]) -> Q:
        category_filter = Q()
        if cat_id:
            selected_cat = get_object_or_404(Category, id=int(cat_id))
            if selected_cat.level < 2:
                id_list = [selected_cat.id]
                children = selected_cat.get_children()
                for child in children:
                    id_list.append(child.id)
                    category_filter &= Q(category__in=id_list)
            else:
                category_filter &= Q(category=selected_cat.id)
        else:
            raise AttributeError('Not found cat_selected.')
        return category_filter

    @staticmethod
    def get_price_filter(price_min: str, price_max: str) -> Q:
        price_filter = Q()
        if price_min != '':
            price_filter &= Q(price__gte=int(price_min))
        if price_max != '':
            price_filter &= Q(price__lte=int(price_max))
        return price_filter

    @staticmethod
    def get_availability_filter(availability: Optional[str]) -> Q:
        availability_filter = Q()
        if availability:
            availability_filter &= Q(availability=True)
        return availability_filter

    @staticmethod
    def get_properties_filter(property_data_list: Optional[List[str]]) -> Q:
        properties_filter = Q()
        if property_data_list:
            properties = {}
            for property in property_data_list:
                values = property.split('_')
                proprety_id = int(values[0])
                if not properties.get(proprety_id):
                    properties[proprety_id] = [values[1]]
                else:
                    properties[proprety_id].append(values[1])
            product_id_queryset = []
            for property_id in properties:
                product_id_queryset += list(PropertyValue.objects
                                            .filter(property=property_id, value__in=properties[property_id])
                                            .values('product').order_by('product'))
            product_id_list = []
            for product in product_id_queryset:
                product_id_list.append(product['product'])
            properties_filter &= Q(id__in=product_id_list)
        return properties_filter

    def get_queryset(self):
        query_dict = self.request.GET
        print(query_dict)

        properties_filter = self.get_properties_filter(query_dict.getlist('properties'))
        category_filter = self.get_category_filter(query_dict.get('cat_selected'))
        availability_filter = self.get_availability_filter(query_dict.get("availability"))
        price_filter = self.get_price_filter(price_min=query_dict.get("price_min"),
                                             price_max=query_dict.get("price_max"))

        queryset = (Product.objects.filter(properties_filter &
                                           category_filter &
                                           price_filter &
                                           availability_filter)
                    .select_related('category')
                    .order_by('-availability', 'name'))
        return queryset

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

        return dict(list(context.items()) + list(c_def.items()))


class Search(DataMixin, ListView):
    # paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get('s')
        return Product.objects.filter(Q(name__icontains=search) | Q(slug__icontains=search)).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Поиск',
                                      path=f"s={self.request.GET.get('s')}&")
        return dict(list(context.items()) + list(c_def.items()))


class ProductDetail(DataMixin, DetailView):
    template_name = 'catalog/product_detail.html'
    slug_url_kwarg = 'prod_slug'
    pk_url_kwarg = 'prod_id'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['product'].name),
                                      cart_product_form=CartAddProductForm())
        return dict(list(context.items()) + list(c_def.items()))



