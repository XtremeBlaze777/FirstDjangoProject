from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib import auth
import os

# Create your tests here.

#setup test cases
class setUpTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

    def test_user_not_logged_in(self):
        response = self.client.get('/polls', follow=True)
        self.assertEqual(response.redirect_chain[0][0], "/polls/")
    
    def unauth_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='stream', password='lg')
        c.login(username='stream', password='lg')
        response = self.client.get('/polls', follow=True)
        self.assertTrue(response.redirect_chain[0][0], "/polls/")

    def test_drop_down_course_selection(self):
        c = Client()
        User.objects.create_user(username='admin', password='admin')
        c.login(username='admin', password='admin')
        response = self.client.get('/polls', follow=True)
        self.assertTrue(response.redirect_chain[0][0], "/polls/")
        
#Google login test
class googleLoginTestCase(TestCase):
    def test_user_not_logged_in(self):
        response = self.client.get('/polls', follow=True)
        self.assertEqual(response.redirect_chain[0][0], "/polls/")
        
#Unauthorized login
class unauthLoginTestCase(TestCase):
    def unauth_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='stream', password='lg')
        c.login(username='stream', password='lg')
        response = self.client.get('/profiles', follow=True)
        self.assertTrue(response.redirect_chain[0][0], "/polls/")

#Unauthorized login 2
class unauthLoginTestCaseTwo(TestCase):
    def unauth_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='stream', password='lg')
        c.login(username='stream', password='lg')
        response = self.client.get('/profiles', follow=True)
        self.assertFalse(response.redirect_chain[0][0], "/services/")

#dropdown menu
class dropdownMenuTestCase(TestCase):
    def unauth_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='admin', password='admin')
        c.login(username='admin', password='admin')
        response = self.client.get('/polls', follow=True)
        self.assertFalse(response.redirect_chain[0][0], "/services/")
