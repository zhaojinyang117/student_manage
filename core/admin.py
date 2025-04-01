from django.contrib import admin
from .models import Teacher, Class, Course, Student, Enrollment


# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject_specialization")
    search_fields = ("name", "email", "subject_specialization")


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "description")
    search_fields = ("name", "year")
    list_filter = ("year",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "teacher", "description")
    search_fields = ("name", "code", "teacher__name")
    list_filter = ("teacher",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "student_id",
        "gender",
        "age",
        "assigned_class",
        "enrollment_date",
    )
    search_fields = ("name", "student_id")
    list_filter = ("gender", "assigned_class", "enrollment_date")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrollment_date", "grade")
    search_fields = (
        "student__name",
        "student__student_id",
        "course__name",
        "course__code",
    )
    list_filter = ("enrollment_date", "course")
