from django.urls import path, include
from users import views

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
]
