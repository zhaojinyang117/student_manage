from django.test import TestCase, Client
from django.urls import reverse
from .models import Teacher, Class, Course, Student, Enrollment

class HomePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 创建测试数据
        self.teacher = Teacher.objects.create(name="测试教师")
        self.class_obj = Class.objects.create(name="测试班级")
        self.course = Course.objects.create(name="测试课程", code="TEST101")
        self.student = Student.objects.create(
            name="测试学生", 
            student_id="TEST001", 
            gender="男", 
            age=18
        )
        
    def test_homepage_view(self):
        """测试主页视图可以正常访问并包含基本数据"""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/homepage.html')
        
        # 检查统计数据是否正确
        self.assertContains(response, '1') # 1个教师
        self.assertContains(response, '1') # 1个班级
        self.assertContains(response, '1') # 1个课程
        self.assertContains(response, '1') # 1个学生

class StudentListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 创建测试数据
        self.class_obj = Class.objects.create(name="测试班级")
        self.course = Course.objects.create(name="测试课程", code="TEST101")
        
        # 创建多个学生以测试列表和搜索功能
        self.student1 = Student.objects.create(
            name="张三", 
            student_id="S001", 
            gender="男", 
            age=18,
            assigned_class=self.class_obj
        )
        self.student2 = Student.objects.create(
            name="李四", 
            student_id="S002", 
            gender="男", 
            age=19
        )
        self.student3 = Student.objects.create(
            name="王五", 
            student_id="S003", 
            gender="女", 
            age=17
        )
        
        # 注册学生到课程
        Enrollment.objects.create(student=self.student1, course=self.course)
        
    def test_student_list_view(self):
        """测试学生列表视图可以正常访问"""
        response = self.client.get(reverse('core:students'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/student_list.html')
        
        # 检查所有学生是否在列表中
        self.assertContains(response, '张三')
        self.assertContains(response, '李四')
        self.assertContains(response, '王五')
        
    def test_student_search(self):
        """测试学生搜索功能"""
        response = self.client.get(f"{reverse('core:students')}?search_term=张三")
        self.assertEqual(response.status_code, 200)
        
        # 应该只包含"张三"，不包含其他学生
        self.assertContains(response, '张三')
        self.assertNotContains(response, '李四')
        self.assertNotContains(response, '王五')
        
    def test_student_filter_by_gender(self):
        """测试性别筛选功能"""
        response = self.client.get(f"{reverse('core:students')}?gender=女")
        self.assertEqual(response.status_code, 200)
        
        # 应该只包含女生"王五"
        self.assertNotContains(response, '张三')
        self.assertNotContains(response, '李四')
        self.assertContains(response, '王五')
        
    def test_student_filter_by_class(self):
        """测试班级筛选功能"""
        response = self.client.get(f"{reverse('core:students')}?class_id={self.class_obj.id}")
        self.assertEqual(response.status_code, 200)
        
        # 应该只包含班级为"测试班级"的学生"张三"
        self.assertContains(response, '张三')
        self.assertNotContains(response, '李四')
        self.assertNotContains(response, '王五')

class CourseViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 创建测试数据
        self.teacher = Teacher.objects.create(name="测试教师")
        self.course1 = Course.objects.create(
            name="数学", 
            code="MATH101", 
            teacher=self.teacher
        )
        self.course2 = Course.objects.create(
            name="物理", 
            code="PHY101"
        )
        
        # 创建学生并将其注册到课程
        self.student1 = Student.objects.create(
            name="张三", 
            student_id="S001", 
            gender="男", 
            age=18
        )
        self.student2 = Student.objects.create(
            name="李四", 
            student_id="S002", 
            gender="女", 
            age=19
        )
        
        Enrollment.objects.create(student=self.student1, course=self.course1, grade=85)
        Enrollment.objects.create(student=self.student2, course=self.course1, grade=92)
        Enrollment.objects.create(student=self.student1, course=self.course2)
        
    def test_course_list_view(self):
        """测试课程列表视图"""
        response = self.client.get(reverse('core:courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/course_list.html')
        
        # 检查所有课程是否在列表中
        self.assertContains(response, '数学')
        self.assertContains(response, '物理')
        
    def test_course_detail_view(self):
        """测试课程详情视图"""
        response = self.client.get(reverse('core:course_detail', args=[self.course1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/course_detail.html')
        
        # 检查课程详情和注册的学生
        self.assertContains(response, '数学')
        self.assertContains(response, '张三')
        self.assertContains(response, '李四')
        
    def test_course_search(self):
        """测试课程搜索功能"""
        response = self.client.get(f"{reverse('core:courses')}?search_term=数学")
        self.assertEqual(response.status_code, 200)
        
        # 应该只包含"数学"，不包含"物理"
        self.assertContains(response, '数学')
        self.assertNotContains(response, '物理')

class ClassViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 创建测试数据
        self.class1 = Class.objects.create(
            name="高一(1)班", 
            year=2023,
            description="文科班"
        )
        self.class2 = Class.objects.create(
            name="高一(2)班", 
            year=2023,
            description="理科班"
        )
        
        # 创建学生并分配到班级
        self.student1 = Student.objects.create(
            name="张三", 
            student_id="S001", 
            gender="男", 
            age=16,
            assigned_class=self.class1
        )
        self.student2 = Student.objects.create(
            name="李四", 
            student_id="S002", 
            gender="女", 
            age=16,
            assigned_class=self.class1
        )
        self.student3 = Student.objects.create(
            name="王五", 
            student_id="S003", 
            gender="男", 
            age=16,
            assigned_class=self.class2
        )
        
        # 创建课程并为学生注册
        self.course1 = Course.objects.create(name="语文", code="CHN101")
        self.course2 = Course.objects.create(name="数学", code="MATH101")
        
        Enrollment.objects.create(student=self.student1, course=self.course1)
        Enrollment.objects.create(student=self.student1, course=self.course2)
        Enrollment.objects.create(student=self.student2, course=self.course1)
        Enrollment.objects.create(student=self.student3, course=self.course2)
        
    def test_class_list_view(self):
        """测试班级列表视图"""
        response = self.client.get(reverse('core:classes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/class_list.html')
        
        # 检查所有班级是否在列表中
        self.assertContains(response, '高一(1)班')
        self.assertContains(response, '高一(2)班')
        
    def test_class_detail_view(self):
        """测试班级详情视图"""
        response = self.client.get(reverse('core:class_detail', args=[self.class1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/class_detail.html')
        
        # 检查班级详情和学生列表
        self.assertContains(response, '高一(1)班')
        self.assertContains(response, '张三')
        self.assertContains(response, '李四')
        self.assertContains(response, '语文')  # 张三和李四都选了语文
        self.assertContains(response, '数学')  # 张三选了数学
        
    def test_class_search_student(self):
        """测试班级详情页中的学生搜索功能"""
        response = self.client.get(f"{reverse('core:class_detail', args=[self.class1.id])}?search_term=张三")
        self.assertEqual(response.status_code, 200)
        
        # 应该只包含"张三"，不包含"李四"
        self.assertContains(response, '张三')
        self.assertNotContains(response, '李四')
        
    def test_class_search(self):
        """测试班级搜索功能"""
        response = self.client.get(f"{reverse('core:classes')}?search_term=文科")
        self.assertEqual(response.status_code, 200)
        
        # 检查是否显示了包含"文科"描述的提示
        self.assertContains(response, '文科') 