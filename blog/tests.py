from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post

User = get_user_model()


class BlogTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            subtitle='Test Subtitle',
            body='This is a test post body.',
            author=self.user
        )

    def test_post_creation(self):
        """Test that a post is created successfully."""
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.title, 'Test Post')

    def test_post_detail_view(self):
        """Test the post detail view."""
        response = self.client.get(reverse('show_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test post body.')

    def test_home_page(self):
        """Test the home page view."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Latest Blog Posts')

    def test_login_view(self):
        """Test the login view."""
        response = self.client.post(
            reverse('login'),
            {'email': self.user.email, 'password': 'testpass'})
        # should redirect after successful login
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        """Test the registration view."""
        response = self.client.post(reverse('register_user'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass',
            'confirm_password': 'newpass'
        })
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
