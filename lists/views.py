from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, pk):
    list_ = List.objects.get(pk=pk)
    items = Item.objects.filter(list=list_)
    return render(request, 'lists/list.html', {'items': items})


def new_list(request):
    list_ = request.POST.get('list', List.objects.create().id)
    list_ = List.objects.get(id=list_)
    item_text = request.POST.get('item_text', '')
    Item.objects.create(text=item_text, list=list_)
    return redirect(f'/lists/{list_.id}')
