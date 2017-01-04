from django.shortcuts import render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):

    if request.method == 'POST':
        newItemText = request.POST['item_text']
        Item.objects.create(text=newItemText)
    else:
        newItemText = ''

    return render(request,'home.html',{
        'new_item_text': newItemText,
    })
