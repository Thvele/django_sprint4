from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Post, Category, Comment
from .forms import EditProfileForm, PostForm, CommentForm
from .utils import get_posts_with_comments, paginate_queryset


def index(request):
    posts = get_posts_with_comments()
    posts = posts.order_by('-pub_date')
    page_number = request.GET.get('page')
    page_obj = paginate_queryset(posts, page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    posts = get_posts_with_comments(category.posts.all())
    posts = posts.order_by('-pub_date')
    page_number = request.GET.get('page')
    page_obj = paginate_queryset(posts, page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not post.is_published and request.user != post.author:
        post = get_object_or_404(get_posts_with_comments(), id=post_id)

    form = CommentForm()
    comments = post.comments.all()

    return render(
        request, 'blog/detail.html', {
            'post': post,
            'form': form,
            'comments': comments,
        }
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)

    filter_published = request.user != profile
    posts = get_posts_with_comments(
        profile.posts.all(), filter_published=filter_published
    )
    posts = posts.order_by('-pub_date')
    page_number = request.GET.get('page')
    page_obj = paginate_queryset(posts, page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/user.html', {'form': form})


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/create.html', {"form": form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next=/posts/{post_id}/edit/")

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.id)

    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post.id)

    return render(request, 'blog/create.html', {"form": form})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('blog:profile', username=request.user.username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:post_detail', post_id=post.id)

    return render(request, 'blog/comment.html', {
        'form': form,
        'post': post
    })


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment, id=comment_id, post_id=post_id, author=request.user
    )
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {
        'form': form,
        'comment': comment
    })


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment, id=comment_id, post_id=post_id, author=request.user
    )
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {
        'comment': comment,
        'post': comment.post
    })


def send_test_email(request):
    send_mail(
        'Тестовое письмо',
        'Это пример тестового письма.',
        'from@example.com',
        ['to@example.com'],
    )
    return HttpResponse(
        'Тестовое письмо отправлено. Проверьте директорию sent_emails/.'
    )
