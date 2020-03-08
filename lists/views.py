from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        item = Item()
        item_text = request.POST.get('item_text', '')
        Item.objects.create(text=item_text)
        return redirect('/')
    else:
        item_text = ''
    return render(request, 'lists/home.html',
                  {'new_item_list': item_text,
                   'items': Item.objects.all()})
