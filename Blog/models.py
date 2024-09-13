from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Blog_Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cat_id}: {self.cat_name}"

class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))  
    email = models.EmailField(verbose_name=_("Email"))  
    message = models.CharField(max_length=255, verbose_name=_("Message"))

    def __str__(self):
        return f'Comment by {self.name}'

class Blog_Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content_1 = models.CharField(max_length=200)
    blog_image = models.ImageField(upload_to='blog_images/')
    blog_image2 = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    content = models.TextField()
    content_1 = models.TextField()
    content_2 = models.TextField()
    conclusion = models.TextField()
    created_on_date = models.DateField(auto_now_add=True)
    created_on_date = models.TimeField(auto_now_add=True)
    author =  models.CharField(max_length=200)
    author_info=models.TextField()
    author_image = models.ImageField(upload_to='author_images/', blank=True, null=True)
    blog_image = models.ImageField(upload_to='blog_images/')
    blog_image2 = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    categories = models.ManyToManyField(Blog_Category)
    comments = models.ManyToManyField(Comment, related_name='blog_posts', blank=True)  # Added blank=True
    def __str__(self):
        return self.title
