from django.db import models
from .utils import create_shortened_url


class Links(models.Model):
    created_date = models.DateField(auto_now_add=True)
    long_url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True, blank=True)
    class Meta:

        ordering = ["-created_date"]


    def __str__(self):

        return f'{self.long_url} to {self.short_url}'

    def save(self, *args, **kwargs):

        # If the short url wasn't specified
        if not self.short_url:
            # We pass the model instance that is being saved
            self.short_url = create_shortened_url(self)

        super().save(*args, **kwargs)

