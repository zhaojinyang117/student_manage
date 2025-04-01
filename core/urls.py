from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomepageView.as_view(), name="index"),  # 首页
    path("students/", views.StudentListView.as_view(), name="students"),  # 学生列表
    path(
        "students/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"
    ),
    path("courses/", views.CourseListView.as_view(), name="courses"),  # 课程列表
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("classes/", views.ClassListView.as_view(), name="classes"),  # 班级列表
    path("classes/<int:pk>/", views.ClassDetailView.as_view(), name="class_detail"),
]
