from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from blog.forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User


# Create your views here.


# Home function
def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'posts': page_obj})


# About function
def about(request):
    return render(request, 'blog/about.html')


# Contact function
def contact(request):
    return render(request, 'blog/contact.html')


# Dashboard function
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(user=request.user)
        userid = request.user
        user = request.user
        full_name = user.get_full_name()
        ip = request.session.get('ip',0)
        return render(request, 'blog/dashboard.html',
                      {'posts': posts, 'full_name': full_name, 'ip': ip, 'userid': userid})
    else:
        return HttpResponseRedirect('/login/')


# logout function
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Signup function
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!!You Have Become Author')
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


# Login function
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !! ')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})

    else:
        return HttpResponseRedirect('/dashboard/')


# Add Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.user = request.user
                pst.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


# Update Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
