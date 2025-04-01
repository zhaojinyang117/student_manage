from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count

from .models import Teacher, Class, Course, Student, Enrollment

# Create your views here.


def index(request):
    """重定向到HomepageView的URL"""
    return HomepageView.as_view()(request)


def students(request):
    """重定向到StudentListView的URL"""
    return StudentListView.as_view()(request)


def courses(request):
    """重定向到CourseListView的URL"""
    return CourseListView.as_view()(request)


def classes(request):
    """重定向到ClassListView的URL"""
    return ClassListView.as_view()(request)


# 学生相关视图
class StudentListView(ListView):
    model = Student
    template_name = "core/student_list.html"
    context_object_name = "students"
    ordering = ["name"]
    paginate_by = 10  # 分页，每页显示10条记录

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("courses").select_related("assigned_class")

        # 处理搜索
        search_term = self.request.GET.get("search_term", "")
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term)
                | Q(student_id__icontains=search_term)
                | Q(assigned_class__name__icontains=search_term)
                | Q(courses__name__icontains=search_term)
            ).distinct()

        # 处理性别筛选
        gender = self.request.GET.get("gender", "")
        if gender:
            queryset = queryset.filter(gender=gender)

        # 处理班级筛选
        class_id = self.request.GET.get("class_id", "")
        if class_id:
            queryset = queryset.filter(assigned_class_id=class_id)

        # 处理课程筛选
        course_id = self.request.GET.get("course_id", "")
        if course_id:
            queryset = queryset.filter(courses__id=course_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "学生列表"
        context["search_term"] = self.request.GET.get("search_term", "")
        context["gender"] = self.request.GET.get("gender", "")
        context["class_id"] = self.request.GET.get("class_id", "")
        context["course_id"] = self.request.GET.get("course_id", "")
        context["all_classes"] = Class.objects.all().order_by("name")
        context["all_courses"] = Course.objects.all().order_by("name")
        return context


class StudentDetailView(DetailView):
    model = Student
    template_name = "core/student_detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"学生详情: {self.object.name}"

        # 获取学生的选课记录和成绩
        enrollments = (
            Enrollment.objects.filter(student=self.object)
            .select_related("course")
            .order_by("course__name")
        )
        context["enrollments"] = enrollments

        return context


# 课程相关视图
class CourseListView(ListView):
    model = Course
    template_name = "core/course_list.html"
    context_object_name = "courses"
    ordering = ["name"]
    paginate_by = 10  # 分页，每页显示10条记录

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("teacher")

        # 处理搜索
        search_term = self.request.GET.get("search_term", "")
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term)
                | Q(code__icontains=search_term)
                | Q(teacher__name__icontains=search_term)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "课程列表"
        context["search_term"] = self.request.GET.get("search_term", "")
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "core/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"课程详情: {self.object.name}"

        # 获取选择该课程的学生列表和对应的成绩
        enrollments = (
            Enrollment.objects.filter(course=self.object)
            .select_related("student")
            .order_by("student__name")
        )
        context["enrollments"] = enrollments

        return context


# 班级相关视图
class ClassListView(ListView):
    model = Class
    template_name = "core/class_list.html"
    context_object_name = "classes"
    ordering = ["name"]
    paginate_by = 10  # 分页，每页显示10条记录

    def get_queryset(self):
        queryset = super().get_queryset()

        # 处理搜索
        search_term = self.request.GET.get("search_term", "")
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) | Q(year__icontains=search_term)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "班级列表"
        context["search_term"] = self.request.GET.get("search_term", "")

        # 为每个班级添加学生人数
        for cls in context["classes"]:
            cls.student_count = cls.students.count()

        return context


class ClassDetailView(DetailView):
    model = Class
    template_name = "core/class_detail.html"
    context_object_name = "class"

    def get_context_data(self, **kwargs):
        """
        准备班级详情页面所需的上下文数据
        包括班级基本信息、学生列表及其选课情况
        支持按学生姓名、学号或课程名称搜索
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"班级详情: {self.object.name}"

        # 使用prefetch_related预先加载所有学生的课程数据，优化查询性能
        students = self.object.students.prefetch_related("courses").order_by("name")

        # 处理搜索功能 - 允许按学生姓名、学号或所选课程搜索
        search_term = self.request.GET.get("search_term", "")
        if search_term:
            # 使用Q对象实现多字段OR条件搜索，支持模糊匹配
            students = students.filter(
                Q(name__icontains=search_term)
                | Q(student_id__icontains=search_term)
                | Q(courses__name__icontains=search_term)
            ).distinct()  # 使用distinct()防止因JOIN产生的重复结果

        # 构建增强的学生数据结构，包含每个学生的选课记录
        students_with_courses = []
        for student in students:
            # 优化：使用select_related一次性加载关联的课程信息，减少查询次数
            enrollments = (
                Enrollment.objects.filter(student=student)
                .select_related("course")  # 预加载关联的课程对象
                .order_by("course__name")  # 按课程名称排序
            )

            # 为每个学生构建包含选课信息的字典
            students_with_courses.append(
                {"student": student, "enrollments": enrollments}
            )

        # 将结果添加到上下文
        context["students_with_courses"] = students_with_courses
        context["search_term"] = search_term
        context["total_students"] = self.object.students.count()  # 班级总人数（不受搜索影响）

        return context


# 主页视图
class HomepageView(TemplateView):
    template_name = "core/homepage.html"

    def get_context_data(self, **kwargs):
        """
        准备首页显示所需的上下文数据
        包括统计计数、课程平均成绩和图表数据
        """
        context = super().get_context_data(**kwargs)

        # 基础统计数据 - 获取各实体的总计数
        context["title"] = "学生管理系统"
        context["student_count"] = Student.objects.count()
        context["teacher_count"] = Teacher.objects.count()
        context["course_count"] = Course.objects.count()
        context["class_count"] = Class.objects.count()

        # 获取课程及其平均成绩 - 优化版本
        # 性能优化：使用批量查询替代循环中的单次查询
        
        # 步骤1: 先一次性获取所有课程对象
        courses = Course.objects.all().order_by("name")
        course_ids = [course.id for course in courses]
        
        # 步骤2: 用单一查询获取所有课程的平均成绩
        # 使用values+annotate组合可以对分组数据进行聚合计算
        avg_grades = (
            Enrollment.objects.filter(course_id__in=course_ids, grade__isnull=False)
            .values('course_id')
            .annotate(avg_grade=Avg('grade'))  # 按课程ID分组计算平均分
            .order_by('course_id')
        )
        
        # 步骤3: 将查询结果转换为字典以优化查找速度
        grade_dict = {item['course_id']: item['avg_grade'] for item in avg_grades}
        
        # 步骤4: 同样用单一查询获取所有课程的学生数量
        student_counts = (
            Enrollment.objects.filter(course_id__in=course_ids)
            .values('course_id')
            .annotate(count=Count('student_id'))  # 按课程ID分组计数
            .order_by('course_id')
        )
        
        # 步骤5: 将学生数量结果也转换为查找字典
        count_dict = {item['course_id']: item['count'] for item in student_counts}
        
        # 步骤6: 组装最终的课程数据列表，使用前面创建的字典快速查找值
        courses_with_avg = []
        for course in courses:
            avg_grade = grade_dict.get(course.id, 0) or 0  # 若无成绩则默认为0
            student_count = count_dict.get(course.id, 0)
            
            courses_with_avg.append(
                {
                    "id": course.id,
                    "name": course.name,
                    "avg_grade": round(avg_grade, 2),  # 四舍五入到两位小数
                    "student_count": student_count,
                }
            )

        context["courses_with_avg"] = courses_with_avg

        # 准备图表数据
        context["chart_labels"] = ["学生", "教师", "课程", "班级"]
        context["chart_data"] = [
            context["student_count"],
            context["teacher_count"],
            context["course_count"],
            context["class_count"],
        ]

        # 课程成绩图表数据
        context["course_names"] = [c["name"] for c in courses_with_avg]
        context["course_avg_grades"] = [c["avg_grade"] for c in courses_with_avg]
        context["course_student_counts"] = [
            c["student_count"] for c in courses_with_avg
        ]

        return context
