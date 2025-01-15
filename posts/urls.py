from django.urls import path
from posts import views


app_name = 'posts'
urlpatterns = [
    path('',views.post_list, name = 'post_list'),
    path('post_create', views.post_create, name = 'post_create'),
    path('<int:pk>/',views.post_detail, name = 'post_detail'),
    path('<int:pk>/update', views.post_update, name = 'post_update'),
    path('<int:pk>/comfirm', views.post_confirm, name = 'post_confirm'),
    path('<int:pk>/delete', views.post_delete, name = 'post_delete')
]