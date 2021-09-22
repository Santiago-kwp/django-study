from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Book
from .forms import BookForm

@require_safe
def index(request):
    books = Book.objects.order_by('-pk')
    context = {
        'books':books,
    }
    return render(request,'books/index.html', context)

@require_http_methods(['GET','POST'])
def create(request):
    if request.method =='POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('books:detail', book.pk)
    else:
        form = BookForm()
    context = {
        'form': form,
    }
    return render(request, 'books/create.html', context)

@require_safe
def detail(request, pk):
    book = Book.objects.get(pk = pk)
    context = {
        'book':book,
    }
    return render(request, 'books/detail.html',context)

@require_http_methods(['GET','POST'])
def update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:detail',pk)
    else:
        form = BookForm(instance=book)
    context = {
        'form':form,
    }
    return render(request, 'books/update.html', context)

@require_POST
def delete(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('books:index')

