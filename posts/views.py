from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post, Comment
from posts.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# pure django

# 게시글 목록
def post_list(request):
    # id 역순으로 게시글을 담아서 template에 전달
    posts = Post.objects.all().order_by('-id')
    context = {
        'posts' : posts
    }
    return render(request, 'posts/post_list.html', context)

# 게시글 작성
# 로그인한 뒤에 작성을 할 수 있게 설정.
@login_required
# 받을 요청의 종류를 "GET","POST" 두 가지로 설정
@require_http_methods(["GET","POST"])
def post_create(request):
    # 요청이 POST일 경우/ 글 작성
    if request.method == "POST":
        # form에 적힌 데이터를 가져옴
        form = PostForm(request.POST)
        # 유효성 검증
        if form.is_valid():
            # 유효하다면 form을 저장
            post = form.save(commit = False)
            # 외래키인 author를 작성한 user로 설정
            post.author = request.user
            # 글 저장
            post.save()
            # 글의 상세 조회 패이지로 연결
            return redirect('posts:post_detail', post.pk)
    else:
        # GET요청일 경우 빈 form을 가져와서 보여줌
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'posts/post_form.html', context)

# 삭제 확인
# 로그인해만 가능
@login_required
def post_confirm(request,pk):
    # 해당 pk의 글을 가져와서 반환
    post = get_object_or_404(Post, pk = pk)
    context = {
        'post':post
    }
    return render(request, 'posts/post_confirm.html', context)

# 게시글 삭제
# 로그인이 필요하고 POST만 요청으로 받음
@login_required
@require_POST
def post_delete(request,pk):
    # 유저가 검증된 유저인지 확인
    if request.user.is_authenticated:
        # 해당 pk의 글을 가져와 삭제
        post = get_object_or_404(Post,pk = pk)
        post.delete()
    # 글 목록 페이지로 연결
    return redirect('posts:post_list')

# 글 상세 조회
def post_detail(request,pk):
    # 해당 pk의 글을 가져옴
    post = get_object_or_404(Post, pk = pk)
    # 페이지에서 댓글 작성할 수 있는 댓글 form을 가져옴
    form = CommentForm()
    # 댓글의 post의 값이 해당 글의 pk인 댓글을 모두 가져옴
    comments = post.comments.all()
    # 댓글의 수를 계산
    comments_count = comments.count()
    # 모두 가져와서 template에 전달달
    context = {
        'post':post,
        'comments':comments,
        'form':form,
        'comments_count':comments_count,
        }
    return render(request, 'posts/post_detail.html', context)


# 글 수정
# 로그인하고 GET과 POST만 요청가능
@login_required
@require_http_methods(['GET','POST'])
def post_update(request, pk):
    # 글을 가져온다. 해당 pk의 글이 없다면 404 에러 반환
    post = get_object_or_404(Post, pk=pk)
    # POST인 경우
    if request.method == "POST":
        # 요청으로 들어온 데이터를 form에 저장
        form = PostForm(request.POST, instance= post)
        # form의 유효성 검증
        if form.is_valid():
            # form 저장
            form.save()
            # 글 상세 조회 페이지 연결
            return redirect('posts:post_detail', post.pk)
    else:
        # 빈 form을 가져와 저장
        form = PostForm(instance = post)
    context = {
        'form':form,
        'post':post
    }
    # 빈 form을 수정 페이지에 전달
    return render(request, 'posts/post_form.html',context)

# 댓글 작성
# 로그인 필요
@login_required
def comments_create(request, pk):
    # 해당 pk의 글을 조회
    post = get_object_or_404(Post, pk = pk)
    # form에 요청의 데이터를 저장
    form = CommentForm(request.POST)
    # 유효성 검증
    if form.is_valid():
        # 댓글에 form 데이터 전달
        comment = form.save(commit = False)
        # 외래키들 설정
        comment.post = post
        comment.author = request.user
        # 댓글 저장
        comment.save()
        return redirect('posts:post_detail', pk)


# 댓글 삭제
# 로그인 해야만 가능
@login_required
def comments_delete(request, post_pk, comment_pk):
    # 해당 pk의 댓글 조회
    comment = Comment.objects.get(pk = comment_pk)
    # 요청이 POST라면 실행
    if request.method == "POST":
        # 댓글 삭제
        comment.delete()
    return redirect('posts:post_detail', pk = post_pk)


# 좋아요 기능
# POST 요청만 허용
@require_http_methods(['POST'])
def like(request, pk):
    # 검증된 유저인지 확인
    if request.user.is_authenticated:
        # 해당 pk의 글을 조회
        post = get_object_or_404(Post, pk=pk)
        # 좋아요 데이터베이스에 유저의 pk가 있는지 확인
        if post.like_users.filter(pk = request.user.pk).exists():
            # 있다면 좋아요 취소
            post.like_users.remove(request.user)
        else:
            # 없다면 좋아요
            post.like_users.add(request.user)
        # 다시 글 상세페이지로 연결
        return redirect("posts:post_detail", pk = post.pk)
    # 로그인 페이지로 연결
    return redirect("users:login")




# DRF
# 글 리스트와 생성
@api_view(['GET','POST'])
def post_list_api(request):
    # 생성 시
    if request.method == 'POST':
        # 유저 확인
        if request.user.is_authenticated:
            # 작성자를 유저로 설정
            request.data["author"] = f"{request.user.id}"
            serializer = PostSerializer(data = request.data)
            # 유효성 검사
            if serializer.is_valid(raise_exception= True):
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)
        # 유저가 아닐 경우
        else: 
            return Response({}, status= status.HTTP_401_UNAUTHORIZED)
    # 요청이 GET일 경우 목록 조회
    else:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)


# 글 상세조회 및 삭제, 수정
@api_view(['GET','PUT','DELETE'])
def post_detail_api(request, pk):
    # 글 불러오기
    post = get_object_or_404(Post, pk = pk)
    # 글 수정
    if request.method == "PUT":
        # 작성자와 유저가 같은 경우
        if request.user == post.author:
            # 변화한 데이터로 직렬화
            serializer = PostDetailSerializer(post, data = request.data, partial = True)
            # 유효성 검사
            if serializer.is_valid(raise_exception= True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({}, status = status.HTTP_401_UNAUTHORIZED)
    # 글 삭제 기능
    elif request.method == 'DELETE':
        # 작성자와 유저가 같은지 판별
        if request.user == post.author:
            # 데이터베이스에서 삭제
            post.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({}, status = status.HTTP_401_UNAUTHORIZED)
    # 글 상세 조회(GET 요청)
    else:
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    

@api_view(['GEt','POST'])
def comments_list_api(request, pk):
    post = get_object_or_404(Post, pk = pk)
    # 댓글 작성
    if request.method == 'POST':
        if request.user.is_authenticated:
            request.data["author"] = f"{request.user.id}"
            serializer = CommentSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(post = post)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response({}, status = status.HTTP_401_UNAUTHORIZED)
    else:
        post = get_object_or_404(Post, pk = pk)
        comments = post.objects.all()
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data)

# 댓글 삭제
@api_view(['DELETE'])
def comments_delete_api(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    if request.user == comment.author:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# 좋아요 기능
@api_view(['POST'])
def like_api(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if post.like_users.filter(pk = request.user.pk).exists():
            post.like_users.remove(request.user)
            return Response({'cancled'}, status = status.HTTP_204_NO_CONTENT)
        else:
            post.like_users.add(request.user)
            return Response({'liked'}, status = status.HTTP_201_CREATED)
    