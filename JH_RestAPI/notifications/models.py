from django.db import models

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(null=True,max_length=250)
    image = models.CharField(null=True, max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']    