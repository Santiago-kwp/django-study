from django.shortcuts import render
from .models import Book

def index(request):
    books = Book.objects.order_by('-pk')
    context = {
        'books':books,
    }
    return render(request,'books/index.html', context)
