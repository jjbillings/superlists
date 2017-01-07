from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List

# Create your views here.
def home_page(request):
    return render(request,'home.html')

def view_list(request, listId):
    list_ = List.objects.get(id=listId)
    return render(request,'list.html',{'list':list_})

def new_list(request):
    list_ = List.objects.create()
    items = Item.objects.create(text=request.POST['item_text'],list=list_)
    return redirect('/lists/%d/'%(list_.id,))

def add_item(request, listId):
    list_ = List.objects.get(id=listId)
    item = Item.objects.create(list=list_,text=request.POST['item_text'])
    return redirect('/lists/%d/'%(list_.id,))
