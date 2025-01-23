from django.urls import path
from posts import views

# 앱 이름
app_name = 'posts'
# url 리스트
urlpatterns = [
    # 글 목록 조회
    path('',views.post_list, name = 'post_list'),
    # 글 작성
    path('post_create', views.post_create, name = 'post_create'),
    # 글 상세 조회
    path('<int:pk>/',views.post_detail, name = 'post_detail'),
    # 글 수정
    path('<int:pk>/update', views.post_update, name = 'post_update'),
    # 글 삭제 확인
    path('<int:pk>/comfirm', views.post_confirm, name = 'post_confirm'),
    # 글 삭제
    path('<int:pk>/delete', views.post_delete, name = 'post_delete')
]