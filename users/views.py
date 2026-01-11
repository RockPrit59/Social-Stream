from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseForbidden

# Forms
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from feed.forms import PostForm, CommentForm

# Models
from feed.models import Post, Message
from .models import Follow, Block  # <--- Added Block

# ---------------------------------------------------------
# AUTHENTICATION & PROFILE SETTINGS
# ---------------------------------------------------------

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)

# ---------------------------------------------------------
# FEED & POSTS
# ---------------------------------------------------------

@login_required
def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    # Get users I blocked or who blocked me
    blocked_users = Block.objects.filter(blocker=request.user).values_list('blocked', flat=True)
    blocked_by_users = Block.objects.filter(blocked=request.user).values_list('blocker', flat=True)
    
    # Filter Feed: Followed users + Self (excluding blocked interactions)
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    
    posts = Post.objects.filter(
        (Q(author__in=following_users) | Q(author=request.user)) &
        ~Q(author__in=blocked_users) &     # Exclude people I blocked
        ~Q(author__in=blocked_by_users)    # Exclude people who blocked me
    ).order_by('-date_posted')

    return render(request, 'users/home.html', {'posts': posts, 'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'users/add_comment.html', {'form': form, 'post': post})

# ---------------------------------------------------------
# POST ACTIONS
# ---------------------------------------------------------

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'users/edit_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('home')
    return render(request, 'users/post_confirm_delete.html', {'post': post})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')

# ---------------------------------------------------------
# SOCIAL & PRIVACY
# ---------------------------------------------------------

@login_required
def search_users(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, 'users/search_results.html', {'results': results, 'query': query})

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user:
        follow_obj = Follow.objects.filter(follower=request.user, following=target_user)
        if follow_obj.exists():
            follow_obj.delete()
        else:
            Follow.objects.create(follower=request.user, following=target_user)
    return redirect('public_profile', username=username)

@login_required
def block_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user:
        block_obj = Block.objects.filter(blocker=request.user, blocked=target_user)
        if block_obj.exists():
            block_obj.delete() # Unblock
            messages.info(request, f'You have unblocked {username}.')
        else:
            Block.objects.create(blocker=request.user, blocked=target_user) # Block
            # Also remove follow connections
            Follow.objects.filter(follower=request.user, following=target_user).delete()
            Follow.objects.filter(follower=target_user, following=request.user).delete()
            messages.warning(request, f'You have blocked {username}.')
            
    return redirect('home')

def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # Check if blocked
    if request.user.is_authenticated:
        if Block.objects.filter(blocker=profile_user, blocked=request.user).exists():
            return render(request, 'users/blocked_error.html', {'user': profile_user})

    # Check Follow Status
    is_following = False
    is_blocked = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
        is_blocked = Block.objects.filter(blocker=request.user, blocked=profile_user).exists()

    # Privacy Logic: Show posts ONLY if public OR (private AND following) OR (it's me)
    show_posts = True
    if profile_user.profile.is_private and not is_following and request.user != profile_user:
        show_posts = False

    user_posts = []
    if show_posts:
        user_posts = Post.objects.filter(author=profile_user).order_by('-date_posted')
    
    context = {
        'profile_user': profile_user,
        'posts': user_posts,
        'is_following': is_following,
        'is_blocked': is_blocked,
        'show_posts': show_posts,
        'follower_count': Follow.objects.filter(following=profile_user).count(),
        'following_count': Follow.objects.filter(follower=profile_user).count()
    }
    return render(request, 'users/public_profile.html', context)

@login_required
def chat_room(request, username):
    other_user = get_object_or_404(User, username=username)
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    return render(request, 'users/chat_room.html', {
        'other_user': other_user, 'chat_messages': messages_list
    })