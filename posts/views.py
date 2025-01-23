from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post
from posts.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST


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
# 로그인해야만 가능
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
    # 해당 pk의 글을 가져와 template에 전달
    post = get_object_or_404(Post, pk = pk)
    context = {
        'post':post,
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
        form = PostForm(request.POST, instance=post)
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