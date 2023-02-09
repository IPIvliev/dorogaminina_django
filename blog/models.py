from django.db import models
from django.utils.text import slugify
from django.utils import timezone 
from django.shortcuts import reverse

class Category(models.Model):
  title = models.CharField("Название категории", max_length=150)
  slug = models.SlugField("SEO адрес", max_length=150, blank=True)
  description = models.TextField("Описание категории", )

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title.lower())
    super(Category, self).save(*args, **kwargs)

  class Meta:
    verbose_name='Категория'
    verbose_name_plural='Категории'

  def __str__(self):
    return self.title

class Article(models.Model):
  title = models.CharField("Название статьи", max_length=350)
  slug = models.SlugField("SEO адрес", max_length=350, blank=True, allow_unicode=True)
  category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_DEFAULT, default=1, related_name='categories_articles')
  article_image = models.FileField(upload_to='uploads/blog/', null=True, blank=True)
  body = models.TextField('Текст статьи', null=True, blank=True)
  publish = models.DateTimeField("Дата публикации", default=timezone.now)
  created = models.DateTimeField("Дата написания статьи", auto_now_add=True)
  updated = models.DateTimeField("Дата изменения статьи", auto_now=True)

  def save(self, *args, **kwargs):
    try:
      self.slug = slugify(self.title, allow_unicode=True)
    except:
      pass
    finally:
      super(Article, self).save(*args, **kwargs)

  class Meta:
    verbose_name = "Статья"
    verbose_name_plural = "Статьи"

  def __str__(self):
    return self.title