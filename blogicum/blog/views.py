from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from .models import Post, Category


def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True
    ).select_related('author',
                     'category',
                     'location').order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=now()
    ).select_related('author', 'location').order_by('-pub_date')
    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)
