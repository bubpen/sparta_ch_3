from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from users.models import User

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:post_list')
        else:
            print('form 검증 실패 : ',form.errors)
    else:
        form = AuthenticationForm()
    context = {'form' : form}   
    return render(request, 'users/login.html', context)

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('posts:post_list')
    
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:post_list')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)

def profile(request, pk):
    user = User.objects.get(pk = pk)
    context = {'user':user}
    return render(request, 'users/profile.html',context)

@login_required
def profile_update(request,pk):
    if request.method == 'POST':
        bio = request.POST.get('bio')
        user = user = User.objects.get(pk = pk)
        user.bio = bio
        user.save()
        return redirect('users:profile', user.pk)
    else:
        user = User.objects.get(pk = pk)
        bio = user.bio
    context = {'bio':bio}
    return render(request, 'users/profile_update.html',context)