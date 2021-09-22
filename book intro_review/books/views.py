from django.shortcuts import render
from .models import Book
from .forms import BookForm

def index(request):
    books = Book.objects.order_by('-pk')
    context = {
        'books':books,
    }
    return render(request,'books/index.html', context)

def create(request):
    if request.method =='POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
    else:
        form = BookForm()
    context = {
        'form': form,
    }
    return render(request, 'books/create.html', context)

