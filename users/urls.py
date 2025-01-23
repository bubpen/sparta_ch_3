from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



app_name = 'users'
urlpatterns = [
    # 로그인
    path('login/', views.login, name = 'login'),
    # 로그아웃
    path('logout/', views.logout, name = 'logout'),
    # 회원가입
    path('signup/', views.signup, name = 'signup'),
    # 프로필 페이지
    path('<int:pk>', views.profile, name = 'profile'),
    # 프로필 수정
    path('<int:pk>/update',views.profile_update, name = 'profile_update'),
    
    # DRF url
    # JWT 토큰 발급
    path("signin/",TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 토큰 갱신
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 회원 가입
    path('api/signup/', views.UserRegistrationView.as_view(), name = 'signup_api'),
    # 로그인
    path('api/login/', views.UserLoginView.as_view(), name = 'login_api'),
    # 로그아웃
    path('api/logout/', views.UserLogoutView.as_view(), name = 'logout_api'),
    # 유저 프로필 페이지 기능
    path('api/<int:pk>/', views.UserProfileAPIVew.as_view(), name = 'profile_api'),
]
