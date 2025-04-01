from django.db import models

"""
学生管理系统核心模型
定义了教师、班级、课程、学生和选课注册之间的关系
"""


class Teacher(models.Model):
    """
    教师模型
    存储教师基本信息，包括姓名、邮箱和专业方向
    与课程形成一对多关系（一名教师可以教授多门课程）
    """
    name = models.CharField(max_length=100, verbose_name="姓名")
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱")
    subject_specialization = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="专业"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = "教师"


class Class(models.Model):
    """
    班级模型
    表示学校中的班级单位，如"高三一班"
    与学生形成一对多关系（一个班级包含多名学生）
    """
    name = models.CharField(max_length=100, verbose_name="班级名称")
    year = models.IntegerField(blank=True, null=True, verbose_name="年份")
    description = models.TextField(blank=True, null=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = "班级"


class Course(models.Model):
    """
    课程模型
    代表学校提供的课程，如"高等数学"
    与教师形成多对一关系（一门课程由一名教师授课）
    与学生通过Enrollment模型形成多对多关系
    """
    name = models.CharField(max_length=100, verbose_name="课程名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="课程代码")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="授课教师",
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "课程"


class Student(models.Model):
    """
    学生模型
    存储学生的基本信息及其班级归属
    与班级形成多对一关系（一名学生属于一个班级）
    与课程通过Enrollment模型形成多对多关系（一名学生可以选多门课程）
    """
    GENDER_CHOICES = [
        ("男", "男"),
        ("女", "女"),
        ("其他", "其他"),
    ]

    name = models.CharField(max_length=100, verbose_name="姓名")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="学号")
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, verbose_name="性别"
    )
    age = models.IntegerField(verbose_name="年龄")
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="注册日期")
    assigned_class = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="所属班级",
    )
    courses = models.ManyToManyField(
        Course, through="Enrollment", related_name="students", verbose_name="选修课程"
    )

    def __str__(self):
        return f"{self.name} ({self.student_id})"

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"


class Enrollment(models.Model):
    """
    选课注册模型
    作为Student和Course之间的中间表，实现多对多关系
    同时存储学生在特定课程中的成绩
    使用unique_together确保一名学生不会重复选同一门课程
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="选课日期")
    grade = models.FloatField(null=True, blank=True, verbose_name="成绩")

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"

    class Meta:
        verbose_name = "课程注册"
        verbose_name_plural = "课程注册"
        unique_together = ("student", "course")
