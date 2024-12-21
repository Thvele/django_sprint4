from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Post, Category, Comment
from django.core.paginator import Paginator
from .forms import EditProfileForm, PostForm, CommentForm
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.utils.timezone import now

def index(request):
    posts = (Post.objects.filter(is_published=True, pub_date__lte=now(),
                                 category__is_published=True)
             .annotate(comment_count=Count('comments'))
             .order_by('-pub_date'))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category,
                                 slug=category_slug,
                                 is_published=True)

    posts = (Post.objects.filter(category=category, is_published=True,
                                 pub_date__lte=now())
             .annotate(comment_count=Count('comments'))
             .order_by('-pub_date'))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not post.is_published and request.user != post.author:
        raise Http404("Пост не найден или доступ запрещён.")

    form = CommentForm()
    comments = post.comments.all()
    return render(request, 'blog/detail.html', {
        'post': post,
        'form': form,
        'comments': comments,
    })


def profile(request, username):
    profile = get_object_or_404(User, username=username)

    if request.user != profile:
        posts = (Post.objects.filter(author=profile,
                                     pub_date__lte=now(),
                                     is_published=True)
                 .annotate(comment_count=Count('comments'))
                 .order_by('-pub_date'))
    else:
        posts = (Post.objects.filter(author=profile)
                 .annotate(comment_count=Count('comments'))
                 .order_by('-pub_date'))



    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
    }

    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'blog/user.html', {'form': form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
        
    return render(request, 'blog/create.html', {"form": PostForm()})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next=/posts/{post_id}/edit/")

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})



@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('blog:profile', username=request.user.username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment.html',
                  {'form': form, 'post': post})


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id,
                                author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html', {'form': form,
                                                 'comment': comment})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id, author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html',
                  {'comment': comment, 'post': comment.post})


def send_test_email(request):
    send_mail(
        'Тестовое письмо',
        'Это пример тестового письма.',
        'from@example.com',
        ['to@example.com'],
    )
    return HttpResponse('Тестовое письмо отправлено. Проверьте директорию sent_emails/.')
