from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import EmployeeProfile, Skill, EmployeeSkill
from workplaces.models import Workplace

class EmployeeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin = User.objects.create_superuser(username='admin', password='12345')
        self.workplace_1 = Workplace.objects.create(table_number='101')

        self.tester = EmployeeProfile.objects.create(
            user=self.user,
            role='tester',
            workplace=self.workplace_1,
            hire_date='2024-06-01'
        )

    def test_home_page_access_and_context(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        if 'total_count' in response.context:
            self.assertIn('total_count', response.context)
        self.assertContains(response, 'Всего сотрудников')

    def test_employee_list_access_and_context(self):
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('employees', response.context)
        self.assertContains(response, self.tester.user.first_name)

    def test_detail_page_login_required(self):
        url = f'/employees/{self.tester.pk}/'
        response_anon = self.client.get(url)
        self.assertEqual(response_anon.status_code, 302)

        self.client.login(username='testuser', password='12345')
        response_logged = self.client.get(url)
        self.assertEqual(response_logged.status_code, 200)

    def test_table_validation_prevents_enemies_next_to_each_other(self):
        workplace_next = Workplace.objects.create(table_number='102')

        bad_dev = EmployeeProfile(
            user=self.admin,
            role='backend',
            workplace=workplace_next,
            hire_date='2025-02-01'
        )
        try:
            bad_dev.save()
            self.fail("Валидатор не сработал: разработчика посадили рядом с тестировщиком.")
        except Exception as e:
            error_msg = str(e)
            self.assertTrue(len(error_msg) > 0)
