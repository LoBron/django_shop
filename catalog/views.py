from django.shortcuts import render

# Create your views here.
def show_all_items(request):
    return render(request, 'catalog/catalog_home.html')