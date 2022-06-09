from django import template
from blog.models import Article

register = template.Library()

@register.simple_tag
def get_news(amount, category=1):
	news = Article.objects.filter(category=category).order_by("-publish")[0:amount]
	return news