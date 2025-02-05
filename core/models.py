from django.db import models
import datetime

# Create your models here.
def assignment_directory_path(instance, filename):
    """
    Generate a custom path for uploaded assignment files.
    
    This function creates a path like:
    'assignments/<year>/<month>/<day>/<filename>'
    
    This helps organize files and prevents potential filename conflicts.
    """
    now = datetime.datetime.now()
    return 'assignments/{0}/{1}/{2}/{3}'.format(now.year, now.month, now.day, filename)

class Assignments(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    file_name = models.FileField(upload_to='assignments/', max_length=100)
    createDate=models.DateField(max_length=100, null=True)

    def __str__(self):
        return self.name
    
class Notice(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    importance = models.CharField(max_length=50, null=True )

    def __str__(self):
      return self.name