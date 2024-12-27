from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(_('Заголовок'), max_length=256)
    description = models.TextField(_('Описание'))
    slug = models.SlugField(_('Идентификатор'), unique=True, help_text=_(
        'Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    ))
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )
    created_at = models.DateTimeField(_('Добавлено'), auto_now_add=True)

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(_('Название места'), max_length=256)
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )
    created_at = models.DateTimeField(_('Добавлено'), auto_now_add=True)

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(_('Заголовок'), max_length=256)
    text = models.TextField(_('Текст'))
    pub_date = models.DateTimeField(
        _('Дата и время публикации'),
        help_text=_('Если установить дату и время в будущем '
                    '— можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Автор публикации'),
        related_name='posts'
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Местоположение')
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=False,
        related_name='posts',
        verbose_name=_('Категория')
    )
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )
    image = models.ImageField(
        _('Изображение'), upload_to='posts/', null=True, blank=True
    )
    created_at = models.DateTimeField(_('Добавлено'), auto_now_add=True)

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        ordering = ['-pub_date', 'title']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name=_('Публикация')
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Автор комментария')
    )
    text = models.TextField(_('Текст комментария'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('комментарий')
        verbose_name_plural = _('Комментарии')
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post}'
