from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from users.models import User

#로그인
def login(request):
    # 요청이 POST인지 확인
    if request.method == "POST":
        # 요청으로부터 데이터를 가져와 form을 채움
        form = CustomAuthenticationForm(data = request.POST)
        # form의 유효성 검증
        if form.is_valid():
            # 로그인 구현
            auth_login(request, form.get_user())
            # 글 목록으로 연결
            return redirect('posts:post_list')
        else:
            # 유효하지 않다면 에러 반환
            print('form 검증 실패 : ',form.errors)
    else:
        # GET 요청일 경우 빈 폼으로 로그인 화면 전달
        form = CustomAuthenticationForm()
    context = {'form' : form}   
    return render(request, 'users/login.html', context)

# 로그아웃
@require_POST
def logout(request):
    # 로그인한 세션을 삭제
    auth_logout(request)
    return redirect('posts:post_list')

# 회원가입
def signup(request):
    # POST 요청일 경우
    if request.method == "POST":
        # 요청의 데이터를 가져와 form을 채우고 유효성 검증 뒤 바로 로그인
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:post_list')
    else:
        # 정보를 채우는 화면을 보여주게 전달
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)

# 유저 프로필 페이지
def profile(request, pk):
    # 유저를 불러와 유저의 정보를 template에 전달
    user = User.objects.get(pk = pk)
    context = {'user':user}
    return render(request, 'users/profile.html',context)

# 유저의 프로필 수정
# 로그인 해야만 가능
@login_required
def profile_update(request,pk):
    if request.method == 'POST':
        # POST 요청일 때 수정된 정보들로 유효성 검증을 마치고 저장하여 다시 프로필 페이지 확인
        form = UserProfileForm(request.POST, instance= request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', pk)
    else:
        # 현재 정보와 함께 수정 페이지 전달
        form  = UserProfileForm()
        context = {'form':form}
    return render(request, 'users/profile_update.html',context)