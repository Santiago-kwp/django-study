from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import 
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash

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


# @login_required
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

@login_required
@require_http_methods(['GET','POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('books:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/password.html', context)
