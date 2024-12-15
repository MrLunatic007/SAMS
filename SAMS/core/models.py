from django.db import models

# Create your models here.
class Exams(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=50)
  start_date = models.DateField(auto_now=False, auto_now_add=False)
  start_time = models.TimeField(auto_now=False, auto_now_add=False)
  end_time = models.TimeField(auto_now=False, auto_now_add=False)

  def __str__(self):
      return self.name

class Assignments(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=150)
  start_date = models.DateField(auto_now=False, auto_now_add=False)
  start_time = models.TimeField(auto_now=False, auto_now_add=False)
  end_time = models.TimeField(auto_now=False, auto_now_add=False)
  file_name = models.FileField(upload_to=None, max_length=100)

  def __str__(self):
      return self.name

class Notice(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    importance = models.CharField(max_length=50, null=True )

    def __str__(self):
      return self.name