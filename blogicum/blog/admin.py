from django.contrib import admin
from .models import Category, Location, Post, Comment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    search_fields = ('title', 'slug')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published',
                    'created_at', 'pub_date')
    search_fields = ('title', 'text')
    list_filter = ('is_published', 'pub_date', 'category')
    date_hierarchy = 'pub_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('text', 'author__username', 'post__title')
    ordering = ('-created_at',)


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name',
                    'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
