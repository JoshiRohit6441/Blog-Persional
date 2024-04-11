from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Blog(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    card_title = models.CharField(max_length=10)
    card_description = models.CharField(max_length=50)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to="blog_images", blank=True, null=True)
    links = models.TextField(blank=True, null=True)
    tags = TaggableManager()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
    scheduled_date = models.DateField(blank=True, null=True)

    def get_schedule_date(self):
        return self.scheduled_date if not self.is_published else None

    def save(self, *args, **kwargs):
        if self.is_published:
            self.scheduled_date = None
        super().save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
