from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)

class Subjects(models.Model):
    SUBJECTS = (
        ('Mathematics'),
        ('English'),
        ('Kiswahili'),
        ('Chemistry'),
        ('Biology'),
        ('Physics'),
        ('Business'),
        ('Computer'),
        ('Geography'),
        ('History'),
        ('Christian Religious Education')
    )

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    class_name = models.CharField(max_length=50)
    guardian_contact = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subjects, related_name='students')

    def __str__(self):
        return f"Student: {self.user.username} (ID: {self.student_id})"


class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=50)
    subjects_taught = models.ManyToManyField(Subjects, related_name='teachers')

    def __str__(self):
        return f"Teacher: {self.user.username} (ID: {self.teacher_id})"