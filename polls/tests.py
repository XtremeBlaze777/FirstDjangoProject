from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib import auth
import os
# Create your tests here.

#Dummy test cases
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

#Google login test cases
class googleLoginTestCase(TestCase):
    def test_user_not_logged_in(self):
        response = self.client.get('/polls', follow=True)
        self.assertEqual(response.redirect_chain[0][0], "/polls/")    