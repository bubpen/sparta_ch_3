from django.urls import path, include
from users import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('signup/', views.signup, name = 'signup'),
    path('<int:pk>', views.profile, name = 'profile'),
    path('<int:pk>/update',views.profile_update, name = 'profile_update'),
]
