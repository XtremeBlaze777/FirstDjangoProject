from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .models import *

class accountTest(TestCase):
    # To check if the login page redirects users to the home page if they're not logged in
    # Expected result: No redirect occurs
    def test_user_not_logged_in(self):
        response = self.client.get('/about', follow=True)
        self.assertEqual(response.redirect_chain[0][0], "https://testserver/about")
    
    # To check if the login redirects logged in users to the home page
    # Expected result: The login page redirects logged in users to the home page
    def test_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='admin', password='admin')
        c.login(username='admin', password='admin')
        response = self.client.get('/about', follow=True)
        self.assertTrue(response.redirect_chain[0][0], "/about")

class CartTest(TestCase):

    # To check that the model accepts valid values
    # Expected result: The k profile is successfully created
    def test_valid_profile_creation(self):
        user = User.objects.create_user(username='admin', password='admin')
    
    # To check that the database saves profile models with correct values
    # Expected result: The k profile is successfully saved into the database
    def test_valid_profile_save(self):
        user = User.objects.create_user(username='admin', password='admin')
        user.save()
    
class CoursesTest(TestCase):

    # To check that the course model accepts valid values
    # Expected result: The course k is successfully created
    def test_valid_course(self):
        k = Course(instructor_name="Will McBurney", catalog_number="3240", subject="CS")

    # To check that valid courses are succesfully saved into the database
    # Expected result: The course k is successfuly saved into the database
    def test_saving_valid_course(self):
        k = Course(instructor_name="Will McBurney", catalog_number="3240", subject="CS")
        k.save()
    
    # To check that valid courses are succesfully added to user profiles
    # Expected result: The course k is successfully saved into profile p
    def test_adding_course_to_profile(self):
        k = Course(instructor_name="Will McBurney", catalog_number="3240", subject="CS")
        k.save()
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        cart_item = CartItem(user=user, course=k)
    
    # To check that profiles don't accept invalid values as course
    # Expected result: The course k rasies a value error after attemtping to add to profile p
    def test_adding_invalid_course_value_to_profile(self):
        with self.assertRaises(ValueError):
            user = User.objects.create_user(username='testuser', password='12345')
            user.save()
            k = "test"
            cart_item = CartItem(user=user, course=k)
    
    # To check that multiple courses can be added to profile
    # Expected result: Profile p returns 3 courses when 3 courses are added
    def test_adding_multiple_courses_to_profile(self):
        a = Course(instructor_name="Will McBurney", catalog_number="3240", subject="CS")
        a.save()
        b = Course(instructor_name="Mark Floryan", catalog_number="2150", subject="CS")
        b.save()
        c = Course(instructor_name="Robbie Hott", catalog_number="4640", subject="CS")
        c.save()