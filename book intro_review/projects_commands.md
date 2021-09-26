## 프로젝트 기본

```bash
$ django-admin startproject naver_books .
$ python manage.py startapp books
# DB 등록하기
$ python manage.py makemigrations
$ python manage.py migrate
# 웹 시작
$ python manage.py runserver
# 관리자 계정 만들기
$ python manage.py createsuperuser
```
`<project_name>/settings.py` 

- 앱 등록하기
- 기본 페이지 탬플릿의 경로 입력하기 (Ex. navbar)
- 정적 파일의 경로 입력하기 (`static`)

```python
INSTALLED_APPS = [
    # local apps
    'books',
    'accounts',
    # 3rd-party library
    'bootstrap5',
    
...
    
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
...
        
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```



`<project_name>/urls.py`

- 앱의 url 등록하기

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
]

```



`templates/base.html`

- static 파일 경로 `load`
- `bootstrap` 파일 링크 ~ `static/bootstrap`
- navbar.html `include`
- 상속받을 html 코드의 블록 지정 `block ~ endblock`

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
      <link rel="stylesheet" type='text/css' href="{% static 'bootstrap/css/bootstrap.min.css' %}">
<body>
  {% include '_navbar.html' %}
  <div class='container'>  
    {% block content %}
    {% endblock %}
  </div>
  <script src="{% static 'bootstrap/js/bootstrap.min.js' %}"></script>

```

`templates/_navbar.html`

- static 파일 경로 `load`
- static 태그를 통해 이미지 파일 경로 설정하기

```html
  {% load static %}
      <a class="navbar-brand m-0 p-0" href="{% url 'books:index' %}">
        <img src="{% static 'images/logo.jpg' %}" alt="Logo Image" width="50em">
```

## 책 정보 CRUD 및 DB 구현하기

`books/urls.py`

- django.urls의 path import 
- 현재 경로의 views.py import
- `app_name` 지정
- `urlpatterns` 지정

```python
from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('',views.index, name='index'),
    path('create/',views.create, name='create'),
    path('<int:pk>/',views.detail, name='detail'),
    path('<int:pk>/update/',views.update, name='update'),
    path('<int:pk>/delete/',views.delete, name='delete'),
]
```



`books/models.py`

- `models.Model` 클래스를 상속받는 DB table 생성 -> 테이블 명 : 앱명_테이블명 (`books_book`)
- 테이블에서 정할 필드속성 정의

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

`books/forms.py`

- django의 `forms` import

- 책 정보를 django의 ModelForm을 상속받아 form 커스터마이징
- label, widget 및 attribute 설정
- 입력이 없는 경우 에러메시지 설정
- 기본 model의 정보를 Meta 클래스로 받아옴

```python
from django import forms
from .models import Book
class BookForm(forms.ModelForm):
    title = forms.CharField(
        label='책 제목',
        widget = forms.TextInput(
            attrs={
                'class': 'my-title form-control',
                'placeholder': '제목을 적어주세요.',
                'maxlength': 100
            }
        ),
        error_messages = {
        'required':'제목이 비었습니다.'
            }
    )
    
...
    class Meta:
        model = Book
        fields = '__all__'
```



`books/views.py`

- `django.shortcut`의 `render` 와 `redirect` import
- 현재 models.py 와 forms.py 에서 DB 정보, 폼 정보를 import
- `django.views.decorators.http`에서 데코레이터를 import
- django ORM 을 통해 DB에서 넘겨줄 데이터를 지정
- 각 함수를 통해 CRUD 로직 구현

```python
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
```



`books/admin.py`

- 등록한 DB 관리자페이지에서 볼 수 있도록 import 및 등록

```python
from .models import Book
admin.site.register(Book)
```



## 로그인 및 회원가입 기능 구현하기

`accounts/urls.py`

- 회원가입, 로그인, 로그아웃, 회원정보 수정 함수 경로 추가
- 패스워드 변경은 따로 url name과 다르게 함수 네이밍

```python
from . import views
app_name = 'accounts'

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('update/',views.update, name='update'),
    path('password/',views.change_password, name='password'),
]
```

`accounts/forms.py`

- 회원가입과 회원정보 수정 폼을 커스터마이징 하기 위해 forms.py 에서 해당 `UserCreationForm` 과 `UserChangeForm`을 import
- `django.contrib.auth`에서 `get_user_model`을 통해 현재 세션에 정의 된 DB 값 가져오기
- Meta 클래스를 통해 해당 form의 필드를 지정하거나 추가하기

```python
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'last_name','first_name')

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email','last_name','first_name')
```



`accounts/views.py`

- `forms.py`에서 지정한 커스터마이징 form import
- 로그인과 비밀번호 수정을 위해 `AuthenticationForm`과 `PasswordChangeForm`을 import
- 로그인과 로그아웃 로직 구현을 위해 `django.contrib.auth`에서 `login, logout`을 import 하면서 alias 지정을 통해 기존 이름과의 충돌 방지
- `UserCreatationForm`의 경우 GET 요청일 경우 인자를 받지 않고, POST일 경우만 request.POST로 인자를 받음
- `auth_login`의 인자는 `request`와 `form.save()`의 리턴 값인 `user`를 활용
- `AuthenticationForm`의 경우 GET 요청일 경우 인자를 받지 않고, POST 요청일 경우 request, request.POST 둘다 인자로 받음
- 유효성 검사 후 자동 로그인을 위해 `auth_login`의 인자로 `request`와 `form.get_user()` attribute를 활용
- 로그아웃은 `POST` 요청이고 현재 로그인 중일 때를 `request.user.is_authenticated`를 통해 판별 후 `auth_logout(request)`를 통해 구현
- 회원정보 수정은 `UserChangeForm`를 사용하여 GET 요청일 경우 `instance=request.user`를 통해 해당 세션 정보를 받아와서 `form`을 통해 넘기고 POST 요청일 경우 `request.POST`인자를 추가함

```python
@require_http_methods(['GET','POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'books:index')

    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/signup.html', context)

@require_http_methods(['GET','POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'books:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/login.html', context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('books:index')

@login_required
@require_http_methods(['GET','POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('books:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/update.html', context)

```



`books/templates/books/index.html`



