from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
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

class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50, primary_key=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    guardian_contact = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subjects, blank=True)  # Many-to-many relationship

    def __str__(self):
        return f"Student: {self.user.username} (ID: {self.student_id})"

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teaching_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    teacher_id = models.CharField(max_length=50, primary_key=True)
    subjects_taught = models.ManyToManyField(Subjects)  # Changed from ForeignKey to ManyToManyField

    def __str__(self):
        return f"Teacher: {self.user.username} (ID: {self.teacher_id})"
    
class ParentProfile(models.Model):
    students_adm = models.ManyToManyField(StudentProfile, related_name='parents')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    parent_id = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return f"Parent Name: {self.user.username} (ID: {self.parent_id})"