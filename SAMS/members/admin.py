from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, TeacherProfile, Subjects

# Register the Subject model
@admin.register(Subjects)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the subject name

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            "fields": (
                'date_of_birth',
                'is_teacher',
                'is_student',
                'is_admin',
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": (
                'date_of_birth',
                'is_teacher',
                'is_student',
                'is_admin',
            ),
        }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'class_name', 'guardian_contact', 'display_subjects')
    list_filter = ('class_name',)  # Add filters for class_name if needed

    # Method to display subjects in the admin
    def display_subjects(self, obj):
        return ", ".join(subject.name for subject in obj.subjects.all())
    display_subjects.short_description = "Subjects"

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id', 'display_subjects_taught')
    list_filter = ('subjects_taught',)  # Add filters for subjects if needed

    # Method to display subjects taught in the admin
    def display_subjects_taught(self, obj):
        return ", ".join(subject.name for subject in obj.subjects_taught.all())
    display_subjects_taught.short_description = "Subjects Taught"
