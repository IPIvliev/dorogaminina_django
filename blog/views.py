from django.shortcuts import render, get_object_or_404
from blog.models import Article
from events.models import Event

def show_article(request, slug, category=None):
  article = get_object_or_404(Article, slug=slug)
  active_event = Event.objects.get(active=True)
  return render(request, 'blog/article.html', {
    'article': article, 
    'title': article.title,
    'event': active_event
  })