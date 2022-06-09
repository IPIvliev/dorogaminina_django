from django.contrib import admin
from django import forms
from blog.models import Article, Category
from ckeditor.widgets import CKEditorWidget

admin.site.register(Category)

class ArticleAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Article
        fields = '__all__'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ['title', 'category']
    search_fields = ['title']
    ordering = ['-publish']