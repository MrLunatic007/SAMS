from django.db import models
import datetime
from django.utils import timezone
from members.models import StudentProfile

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
    due_date = models.DateField(default=timezone.now)
    file_name = models.FileField(upload_to='assignments/', max_length=100)
    createDate=models.DateField(max_length=100, null=True)

    def __str__(self):
        return self.name

class AssignmentSubmission(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name='student_submissions')
    submission_file = models.FileField(upload_to='submissions/%Y/%m/%d/', blank=True, null=True)
    answer_text = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('late', 'Late Submission'),
            ('graded', 'Graded')
        ],
        default='draft'
    )
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    teacher_feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'assignment']
        ordering = ['-submitted_at']

def save(self, *args, **kwargs):
    if self.status == 'submitted':
        due_date = self.assignment.due_date
        
        # Ensure due_date is a datetime object
        if isinstance(due_date, timezone.datetime):
            due_datetime = due_date
        else:
            due_datetime = timezone.make_aware(
                timezone.datetime.combine(due_date, timezone.datetime.min.time())
            )

        if due_datetime < timezone.now():
            self.status = 'late'

    super().save(*args, **kwargs)

    
class Notice(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    importance = models.CharField(max_length=50, null=True )

    def __str__(self):
      return self.name