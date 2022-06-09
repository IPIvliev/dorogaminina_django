from django import template
from blog.models import Article

register = template.Library()

@register.simple_tag
def get_news(amount):
	news = Article.objects.filter(category=1).order_by("-publish")[0:amount]
	return news