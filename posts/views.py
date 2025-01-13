from django.shortcuts import render, redirect
from posts.models import Post


def post_list(request):
    post = Post.objects.all()
    context = {
        'post' : post
    }
    return render(request, 'posts/post_list.html', context)
