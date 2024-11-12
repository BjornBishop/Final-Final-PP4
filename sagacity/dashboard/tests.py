
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Assignment
from .forms import SignUpForm, AssignmentForm
from decimal import Decimal

# Tests go below here

# Modal tests
class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpass123'
        )
        
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            industry='FS',
            duration=30,
            rate=Decimal('500.00'),
            currency='EUR',
            requirements='Python/Django/Testing',
            description='Test description',
            created_by=self.user
        )

    def test_assignment_creation(self):
        """Test assignment instance creation"""
        self.assertEqual(self.assignment.title, 'Test Assignment')
        self.assertTrue(isinstance(self.assignment, Assignment))
        self.assertEqual(str(self.assignment), 'Test Assignment')

    def test_assignment_is_active_default(self):
        """Test assignment is_active defaults to True"""
        self.assertTrue(self.assignment.is_active)

# Form Tests

class FormTests(TestCase):
    def test_signup_form_valid_data(self):
        """Test SignUpForm with valid data"""
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid_data(self):
        """Test SignUpForm with invalid data"""
        form_data = {
            'first_name': '',  # Required field
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'different'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_assignment_form_valid_data(self):
        """Test AssignmentForm with valid data"""
        form_data = {
            'title': 'Test Assignment',
            'industry': 'FS',
            'duration': 30,
            'rate': '500.00',
            'currency': 'EUR',
            'requirements': 'Requirement 1/Requirement 2',
            'description': 'Valid description without contact info'
        }
        form = AssignmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_assignment_form_invalid_contact_info(self):
        """Test AssignmentForm rejects contact information in description"""
        form_data = {
            'title': 'Test Assignment',
            'industry': 'FS',
            'duration': 30,
            'rate': '500.00',
            'currency': 'EUR',
            'requirements': 'Requirement 1/Requirement 2',
            'description': 'Contact me at test@example.com'
        }
        form = AssignmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

# View Tests

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpass123'
        )
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            industry='FS',
            duration=30,
            rate=Decimal('500.00'),
            currency='EUR',
            requirements='Python/Django/Testing',
            description='Test description',
            created_by=self.user
        )

    def test_home_view(self):
        """Test home view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')

    def test_signup_view(self):
        """Test signup view and form submission"""
        # Test GET request
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/signup.html')

        # Test POST request with valid data
        signup_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'phone_number': '1234567890',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_assignment_detail_view(self):
        """Test assignment detail view"""
        # Test unauthenticated access
        response = self.client.get(reverse('assignment_detail', args=[self.assignment.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test authenticated access
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('assignment_detail', args=[self.assignment.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/assignment_detail.html')

    def test_my_assignments_view(self):
        """Test my assignments view"""
        # Test unauthenticated access
        response = self.client.get(reverse('my_assignments'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test authenticated access
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('my_assignments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/my_assignments.html')

    def test_create_assignment_view(self):
        """Test create assignment view and form submission"""
        self.client.login(username='testuser@example.com', password='testpass123')
        
        # Test GET request
        response = self.client.get(reverse('create_assignment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/create_assignment.html')

        # Test POST request with valid data
        assignment_data = {
            'title': 'New Test Assignment',
            'industry': 'FS',
            'duration': 30,
            'rate': '500.00',
            'currency': 'EUR',
            'requirements': 'Requirement 1/Requirement 2',
            'description': 'Valid description'
        }
        response = self.client.post(reverse('create_assignment'), assignment_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Assignment.objects.filter(title='New Test Assignment').exists())

    def test_delete_assignment(self):
        """Test assignment deletion"""
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.post(reverse('delete_assignment', args=[self.assignment.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Assignment.objects.filter(pk=self.assignment.pk).exists())

    def test_toggle_assignment(self):
        """Test assignment activation/deactivation"""
        self.client.login(username='testuser@example.com', password='testpass123')
        self.assertTrue(self.assignment.is_active)  # Initially active
        
        # Test deactivation
        response = self.client.post(reverse('toggle_assignment', args=[self.assignment.pk]))
        self.assignment.refresh_from_db()
        self.assertFalse(self.assignment.is_active)
        
        # Test activation
        response = self.client.post(reverse('toggle_assignment', args=[self.assignment.pk]))
        self.assignment.refresh_from_db()
        self.assertTrue(self.assignment.is_active)