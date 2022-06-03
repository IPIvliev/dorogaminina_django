# Generated by Django 4.0.4 on 2022-06-03 14:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='category',
            name='wp_term_id',
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=350, verbose_name='Название статьи')),
                ('slug', models.SlugField(blank=True, max_length=350, verbose_name='SEO адрес')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Текст статьи')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата написания статьи')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения статьи')),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='categories_articles', to='blog.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
