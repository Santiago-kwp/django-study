from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm, CommentForm
# Create your views here.

def index(request):
    articles = Article.objects.all()
    comment_form = CommentForm()
    context = {
        'articles':articles,
        'comment_form':comment_form,
    }
    return render(request, 'articles/index.html', context)

def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    
    context = {
        'article_form':article_form,
    }
    return render(request, 'articles/create.html', context)

@login_required
@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('articles:index')

def comment_create(request, article_pk):
    # article 인스턴스를 이용해서 저장
    # comment_form = CommentForm(request.POST)
    # article = Article.objects.get(pk=article_pk)

    # if comment_form.is_valid():
    #     comment = comment_form.save(commit=False)
    #     comment.article = article
    #     comment.save()
    #     return redirect('articles:index')

    # article_id를 이용해서 저장하기
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article_id = article_pk
        comment.save()
        return redirect('articles:index')
