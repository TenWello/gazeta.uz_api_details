from django.db import models

class GazetaNews(models.Model):
    title     = models.CharField(max_length=300)
    link      = models.URLField(unique=True, max_length=500)
    time_ago  = models.CharField(max_length=100)
    full_text = models.TextField()
    image     = models.URLField(max_length=500, blank=True)      
    images    = models.JSONField(default=list, blank=True)     
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
