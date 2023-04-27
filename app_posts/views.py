from audioop import reverse
from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app_login.models import UserProfile,Follow
from django.contrib.auth.models import User
from .models import Post,Like
ty
# Create your views here.
@login_required
def home(request):
    follower = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=follower.values_list('following'))
    # The home html does not have the keys of where the following or the following is supposed to occur hence, a valued list is used to connect them
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post',flat=True)

    if request.method == 'GET':
        search = request.GET.get('search','')
        result = User.objects.filter(username__icontains=search)
    return render(request,'app_posts/home.html', context = {'title':'Home Page','search':search,'result':result,'posts':posts,'liked_post_list':liked_post_list})

@login_required
def liked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post,user=request.user)
    if not already_liked:
        like_post=Like(post=post,user=request.user)
        like_post.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def unliked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post,user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('home'))
