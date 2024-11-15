# app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, Like, Comment
from .forms import SignUpForm, LoginForm, ProfileForm, PostForm, CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseForbidden, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

def home(request):
    posts_list = Post.objects.all().order_by('-created_at') 
    paginator = Paginator(posts_list, 5) 

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'home.html', {'posts': posts})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        
        user.save() 
        return redirect('profile')  

    return render(request, 'profile.html', {'user': request.user})

def my_posts(request):
    user_posts = Post.objects.filter(user=request.user)
    posts_count = user_posts.count() 
    return render(request, 'my_posts.html', {
        'posts': user_posts,
        'posts_count': posts_count,
        'user': request.user
    })


def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()
            return redirect('home')  
    else:
        form = PostForm()
    
    return render(request, 'new_post.html', {'form': form})

@login_required
def download_file(request, post_id):
    """Allows the user to download the file associated with a post."""
    post = get_object_or_404(Post, id=post_id)

    if not post.file:
        messages.error(request, "No file is attached to this post.")
        return redirect('home')  # Redirect to an appropriate page

    file_path = post.file.path
    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{post.file.name.split("/")[-1]}"'
            return response
    except FileNotFoundError:
        messages.error(request, "The file is missing.")
        return redirect('home')


def search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(user__username__icontains=query) |
            Q(content__icontains=query) |
            Q(title__icontains=query) |
            Q(file__icontains=query)
        )
    else:
        posts = Post.objects.none()  
    
    return render(request, 'search_results.html', {'posts': posts, 'query': query})


from .forms import CommentForm  

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  
    
   
    file_type = None
    if post.file:
        if post.file.url.endswith(('.jpg', '.jpeg', '.png')):
            file_type = 'image'
        elif post.file.url.endswith(('.mp4', '.webm')):
            file_type = 'video'
        elif post.file.url.endswith(('.mp3', '.wav')):
            file_type = 'audio'
    
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user  
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'file_type': file_type,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    return redirect('post_detail', post_id=post.id)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    post.delete()
    return redirect('my_posts')