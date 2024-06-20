from django.conf import settings
from django.db import models
from django.utils.text import slugify

# Create your models here.
"""
This is the model that we will use to store images in the platform
"""


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created']), ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    """
    override save function to automatically generate the slug field based
    on the value of the title field
    """
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)