from celery import shared_task
from datetime import date
from .models import Blog


@shared_task
def published_blog():
    today = date.today()
    blogs = Blog.objects.filter(is_published=False, scheduled_date=today)
    for blog in blogs:
        blog.is_published = True
        blog.save()
