from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post
from posts.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST

def post_list(request):
    posts = Post.objects.all().order_by('-id')
    context = {
        'posts' : posts
    }
    return render(request, 'posts/post_list.html', context)

@login_required
@require_http_methods(["GET","POST"])
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'posts/post_form.html', context)


@login_required
def post_confirm(request,pk):
    post = get_object_or_404(Post, pk = pk)
    context = {
        'post':post
    }
    return render(request, 'posts/post_confirm.html', context)


@require_POST
def post_delete(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk = pk)
        post.delete()
    return redirect('posts:post_list')

def post_detail(request,pk):
    post = get_object_or_404(Post, pk = pk)
    comments = post.comments.all()
    context = {
        'post':post,
        'comments':comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
@require_http_methods(['GET','POST'])
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit = False)
            return redirect('posts:post_detail', post.pk)
    else:
        form = PostForm(instance = post)
    context = {
        'form':form,
        'post':post
    }
    return render(request, 'posts/post_form.html',context)