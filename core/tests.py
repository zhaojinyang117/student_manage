from django.test import TestCase
from django.db import IntegrityError
from .models import Teacher, Class, Course, Student, Enrollment

# Create your tests here.

class TeacherModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            name="张教授",
            email="zhang@example.com",
            subject_specialization="数学"
        )
    
    def test_teacher_creation(self):
        self.assertEqual(self.teacher.name, "张教授")
        self.assertEqual(self.teacher.email, "zhang@example.com")
        self.assertEqual(self.teacher.subject_specialization, "数学")
    
    def test_teacher_string_representation(self):
        self.assertEqual(str(self.teacher), "张教授")

class ClassModelTest(TestCase):
    def setUp(self):
        self.class_obj = Class.objects.create(
            name="高三一班",
            year=2023,
            description="理科班"
        )
    
    def test_class_creation(self):
        self.assertEqual(self.class_obj.name, "高三一班")
        self.assertEqual(self.class_obj.year, 2023)
        self.assertEqual(self.class_obj.description, "理科班")
    
    def test_class_string_representation(self):
        self.assertEqual(str(self.class_obj), "高三一班")

class CourseModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="李老师", email="li@example.com")
        self.course = Course.objects.create(
            name="高等数学",
            code="MATH101",
            description="微积分入门",
            teacher=self.teacher
        )
    
    def test_course_creation(self):
        self.assertEqual(self.course.name, "高等数学")
        self.assertEqual(self.course.code, "MATH101")
        self.assertEqual(self.course.description, "微积分入门")
        self.assertEqual(self.course.teacher, self.teacher)
    
    def test_course_string_representation(self):
        self.assertEqual(str(self.course), "高等数学 (MATH101)")
    
    def test_unique_code(self):
        # 测试课程代码唯一性约束
        with self.assertRaises(IntegrityError):
            Course.objects.create(
                name="高等数学II",
                code="MATH101",  # 重复的代码
                description="微积分进阶"
            )

class StudentModelTest(TestCase):
    def setUp(self):
        self.class_obj = Class.objects.create(name="高二三班", year=2024)
        self.student = Student.objects.create(
            name="王小明",
            student_id="S202401",
            gender="男",
            age=18,
            assigned_class=self.class_obj
        )
        self.course = Course.objects.create(name="物理", code="PHY101")
    
    def test_student_creation(self):
        self.assertEqual(self.student.name, "王小明")
        self.assertEqual(self.student.student_id, "S202401")
        self.assertEqual(self.student.gender, "男")
        self.assertEqual(self.student.age, 18)
        self.assertEqual(self.student.assigned_class, self.class_obj)
        self.assertTrue(hasattr(self.student, 'enrollment_date'))
    
    def test_student_string_representation(self):
        self.assertEqual(str(self.student), "王小明 (S202401)")
    
    def test_unique_student_id(self):
        # 测试学号唯一性约束
        with self.assertRaises(IntegrityError):
            Student.objects.create(
                name="李小红",
                student_id="S202401",  # 重复的学号
                gender="女",
                age=17
            )

class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="张三",
            student_id="S202402",
            gender="男",
            age=19
        )
        self.course = Course.objects.create(name="英语", code="ENG101")
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            grade=85.5
        )
    
    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.course, self.course)
        self.assertEqual(self.enrollment.grade, 85.5)
        self.assertTrue(hasattr(self.enrollment, 'enrollment_date'))
    
    def test_enrollment_string_representation(self):
        self.assertEqual(str(self.enrollment), "张三 - 英语")
    
    def test_unique_student_course(self):
        # 测试学生-课程组合的唯一性约束
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(
                student=self.student,
                course=self.course,
                grade=90.0
            )
