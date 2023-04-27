from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateNewUser, EditProfile
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from app_login.models import UserProfile,Follow
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from app_posts.forms import PostForm
from django.contrib.auth.models import User



# Create your views here.
def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data = request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profie = UserProfile(user=user)
            user_profie.save()
            return HttpResponseRedirect(reverse('app_login:login'))

    return render(request, 'app_login/signup.html', context = {'title': 'Signup Form Here','form':form})



def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('app_posts:home'))


    return render(request, 'app_login/login.html', context = {'title': 'Login Page', 'form': form})





@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)

    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('app_login:profile'))

    return render(request,'app_login/profile.html', context = {'title':'Edit Profile Page','form':form})



@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('app_login:login'))



@login_required
def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('app_login:profile'))

    return render(request, 'app_login/user.html', context = {'title':'User Profile','form':form})


@login_required
def user(request,username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=user_other,following=request.user) 
    # The key on the requested page should match the key on the like or unlike botton, sensibly, cause those buttons are peculiar to the page hence the key used
    if user == request.user:
        return HttpResponseRedirect(reverse('app_login:profile'))
    return render(request, 'app_login/user_other.html', context={'user_other':user_other,'already_followed':already_followed})


@login_required
def follow(request, username):
    following_user =  request.user
    follower_user = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=follower_user,following=following_user) 
    # Well the concept of following and liking is very simple, it just correlates,mathches or juxtaposes the current user as the follower with the viewed user as the following when clicked :)
    if not already_followed:
        followed_user = Follow(follower=follower_user,following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('app_login:user',kwargs={'username':username}))



@login_required
def unfollow(request,username):
    following_user =  request.user
    follower_user = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=follower_user,following=following_user) 
    already_followed.delete()
    return HttpResponseRedirect(reverse('app_login:user',kwargs={'username':username}))