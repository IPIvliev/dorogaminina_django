from django.contrib import admin
from blog.models import Article, Category

admin.site.register(Category)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    search_fields = ['title']
    ordering = ['-publish']