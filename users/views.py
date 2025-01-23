from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# 로그인
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
def profile_update(request, pk):
    if request.method == 'POST':
        # POST 요청일 때 수정된 정보들로 유효성 검증을 마치고 저장하여 다시 프로필 페이지 확인
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', pk)
    else:
        # 현재 정보와 함께 수정 페이지 전달
        form = UserProfileForm(instance = request.user)
    context = {'form':form}
    return render(request, 'users/profile_update.html',context)


# DRF
# 회원가입
 # 이 뷰는 DRF의 CreateView를 상속받아 회원가입 기능을 구현
class UserRegistrationView(generics.CreateAPIView):
    # 요청 데이터의 검증과 저장을 담당할 직렬화 클래스 지정
    serializer_class = UserSerializer

# 로그인
class UserLoginView(generics.GenericAPIView):
    # 요청 데이터 검증에 사용할 직렬화 클래스 지정
    serializer_class = UserSerializer

    # POST 요청을 처리하는 메서드 : 사용자 인증을 처리하고, JWT 토큰을 반환환
    def post(self, request, *args, **kwargs):
        # 클라이언트에서 보낸 데이터를 직렬화 클래스를 통해 검증
        serializer = self.get_serializer(data=request.data)
        # 데이터가 유효한지 검사하고, 유효하지 않을 경우 400 에러를 반환
        serializer.is_valid(raise_exception=True)
        # 검증된 데이터를 가져와 여기에 유저 정보를 포함
        user = serializer.validated_data

        # 유효한 사용자에 대해 새 JWT RefreshToken 생성성
        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        # 클라이언트에게 JWT 토큰을 포함한 응답 반환
        return Response(response)

# 로그아웃
class UserLogoutView(APIView):
    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    # POST 요청을 처리하는 메서드
    def post(self, request, *args, **kwargs):
        try:
            # 요청에서 Refresh 토큰 가져오기
            refresh_token = request.data.get('refresh')
            # 제공된 Refresh 토큰 문자열을 기반으로 RefreshToken 객체를 생성성
            token = RefreshToken(refresh_token)
            # 토큰을 Blacklist에 추가
            token.blacklist()
            # 로그아웃이 잘 처리되었음을 응답으로 보냄냄
            return Response({"message": "Successfully logged out."}, status=204)
        except Exception as e:
            # 예외 발생 시 오류 메세지를 포함한 응답 반환
            return Response({"error": str(e)}, status=400)


class UserProfileAPIVew(APIView):
    def get(self, request, pk):
        # 해당 pk의 유저를 불러와 직렬화
        user = get_object_or_404(User, pk = pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)