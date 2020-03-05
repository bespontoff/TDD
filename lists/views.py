from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, 'lists/home.html',
                  {'new_item_list': request.POST.get('item_text')})
