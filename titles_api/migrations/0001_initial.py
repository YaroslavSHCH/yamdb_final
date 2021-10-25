# Generated by Django 3.0.5 on 2021-07-27 22:01

import django.core.validators
import django.db.models.deletion
import titles_api.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter name of a category', max_length=50, verbose_name='Categories name')),
                ('slug', models.SlugField(default='djangodbmodelsfieldscharfield', help_text='Create slug for a category', unique=True, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter name of a genre', max_length=50, verbose_name='Genres name')),
                ('slug', models.SlugField(default='djangodbmodelsfieldscharfield', help_text='Create slug for a genre', unique=True, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Enter name of a Title', max_length=150, verbose_name='Title name')),
                ('year', models.PositiveIntegerField(validators=[titles_api.validators.year_validator])),
                ('description', models.TextField(blank=True, help_text='Description of title, put here', max_length=2000, null=True, verbose_name='Description of title')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='titles_api.Category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(blank=True, related_name='titles', to='titles_api.Genre', verbose_name='Genre of a Title')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text review')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date published')),
                ('score', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10, 'Score can be only between 0 to 10'), django.core.validators.MinValueValidator(1, 'Score can be only between 0 to 10')], verbose_name='Score')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='titles_api.Title', verbose_name='Review of title')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text of comment')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='titles_api.Review')),
            ],
            options={
                'verbose_name_plural': 'comments',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='restrict_multiple_review'),
        ),
    ]