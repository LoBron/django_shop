from django.shortcuts import render

# Create your views here.
def show_all_items(request):
    return render(request, 'news/news_home.html')