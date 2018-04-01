from django.db import models

# Create your models here.
class CourseRepository(models.Model):
    key = models.SlugField(unique=True)
    git_origin = models.CharField(max_length=255, default='')
    git_branch = models.CharField(max_length=50, default='')
    name = models.CharField(max_length=50, default='')
    owner = models.CharField(max_length=30, default='')

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name

class CourseRepositoryUpdate(models.Model):
    repo = models.ForeignKey(CourseRepository, on_delete=models.CASCADE, related_name="updates")
    request_ip = models.CharField(max_length=50)
    request_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    updated = models.BooleanField(default=False)
    log = models.TextField(default='')

    class META:
        ordering = ['-request_time']

    # LISÄÄ VIELÄ LOG
