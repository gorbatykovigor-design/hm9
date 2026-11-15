from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.views.decorators.cache import cache_page






def home(request):
    return HttpResponse("Здарова всім")


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts':posts})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments})




@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            time_limit = timezone.now() - timedelta(minutes=5)

            comments_count = Comment.objects.filter(
                author=request.user,
                date__gte=time_limit
            ).count()

            if comments_count >= 3:
                form.add_error(None, "Можна залишити тільки 3 коментарі за 5 хвилин!")
            else:
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                return redirect('post_detail', post_id=post.id)

    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form})








def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})









@cache_page(300)
def post_list(request):
    posts = Post.objects.select_related('author')

    return render(request, 'posts.html', {
        'posts': posts
    })
# Create your views here.
