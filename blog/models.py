from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    """Blog post model."""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    img_url = models.URLField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'post_id': self.pk})


class Comments(models.Model):
    """Comments linked to posts and users."""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    the_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comments'
    )
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date']

    def __str__(self):
        who = self.the_user.username if self.the_user else 'Anonymous'
        return f'Comment by {who} on {self.post.title}'
