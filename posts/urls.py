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
    path('<int:pk>/delete', views.post_delete, name = 'post_delete'),
    # 좋아요 기능
    path('<int:pk>/like/',views.like, name = 'like'),
    # 댓글 작성
    path('<int:pk>/comments/', views.comments_create, name = 'comments_create'),
    # 댓글 삭제
    path('<int:post_pk>/comment_delete/<int:comment_pk>', views.comments_delete, name = 'comments_delete'),
    
    
    # DRF
    # 글 목록 조회/ 작성
    path('api/', views.post_list_api, name = 'post_list_api'),
    # 글 상세조회/수정/삭제
    path('api/<int:pk>/',views.post_detail_api, name = 'post_detail_api'),
    # 댓글 목록 조회/작성
    path('api/<int:pk>/comments/', views.comments_list_api, name = 'comments_lsi_api'),
    # 특정 댓글 삭제
    path('api/comments/<int:pk>/', views.comments_delete_api, name = 'comments_update_api'),
    # 좋아요 기능
    path('api/<int:pk>/like/', views.like_api, name = 'like_api'),
]