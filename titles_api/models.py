from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from .validators import year_validator

User = get_user_model()


class Category(models.Model):
    """Класс описывает модель Категории для Тайтла."""
    name = models.CharField(
        verbose_name='Categories name',
        help_text='Enter name of a category',
        max_length=50
    )
    slug = models.SlugField(verbose_name='Slug',
                            help_text='Create slug for a category',
                            max_length=50,
                            unique=True,
                            default=slugify(name))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.slug


class Genre(models.Model):

    name = models.CharField(
        verbose_name='Genres name',
        help_text='Enter name of a genre',
        max_length=50
    )
    slug = models.SlugField(
        verbose_name='Slug',
        help_text='Create slug for a genre',
        max_length=50,
        unique=True,
        default=slugify(name)
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.slug


class Title(models.Model):

    name = models.CharField(
        verbose_name='Title name',
        help_text='Enter name of a Title',
        max_length=150,
        db_index=True
    )
    year = models.PositiveIntegerField(
        validators=[year_validator]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Genre of a Title'
    )
    description = models.TextField(
        verbose_name='Description of title',
        help_text='Description of title, put here',
        max_length=2000,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.ForeignKey(
        'Title',
        verbose_name='Review of title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField(verbose_name='Text review')
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )
    score = models.IntegerField(
        'Score',
        validators=[
            MaxValueValidator(10, 'Score can be only between 0 to 10'),
            MinValueValidator(1, 'Score can be only between 0 to 10'),
        ]
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='restrict_multiple_review',
            ),
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Text of comment')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text[:15]
