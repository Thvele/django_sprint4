from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from .models import Post


def paginate_queryset(queryset, page_number, per_page=10):
    paginator = Paginator(queryset, per_page)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def get_posts_with_comments(queryset=None, filter_published=True):
    if queryset is None:
        queryset = Post.objects.all()

    if filter_published:
        queryset = queryset.filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True
        )

    return queryset.annotate(comment_count=Count('comments')).order_by(
        *Post._meta.ordering
    )
