from django.http import request
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from womans.models import Womens


def womens_home(request):

    womens = Womens.objects.all()

    return render(request, 'womans/womens_home.html', {'womens': womens})

class WomensDetailView(DetailView):
    model = Womens
    template_name = 'womans/details_view.html'
    context_object_name = 'womens_detail'