from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    list_display = ['pk', 'name', 'year', 'genres', 'category', 'description']
    search_fields = ['name', 'genre', 'category']
    list_filter = ['name', 'genre', 'category']
    empty_value_display = '-пусто-'

    def genres(self, obj):
        return list(obj.genre.values_list('slug', flat=True))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug']
    search_fields = ['name']
    list_filter = ['name']
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug']
    search_fields = ['name']
    list_filter = ['name']
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'author', 'text', 'score']
    search_fields = ['title', 'author']
    list_filter = ['title', 'author']
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'review', 'author', 'text', 'pub_date']
    search_fields = ['review']
    list_filter = ['review']
    empty_value_display = '-пусто-'
