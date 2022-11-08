from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.dispatch import receiver
from django.shortcuts import reverse


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField('CartItem')
    total_units = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user.username) 



class Department(models.Model):
    deptJson = models.JSONField(default=dict)

class Course(models.Model):
    instructor_name = models.CharField(max_length = 150, default="")
    instructor_email = models.EmailField(max_length=254, default="sample@email.com")
    course_number = models.PositiveIntegerField(default=0)
    course_section = models.CharField(max_length = 8, default="")
    subject = models.CharField(max_length = 5, default="")
    catalog_number = models.CharField(max_length=7, default="")
    description=models.TextField(max_length=254, default="")
    units = models.CharField(max_length=10, default="")
    component = models.CharField(max_length=10, default="")
    class_capacity = models.PositiveIntegerField(default=0)
    wait_list = models.PositiveIntegerField(default=0)
    wait_cap = models.PositiveIntegerField(default=0)
    enrollment_total = models.PositiveIntegerField(default=0)
    enrollment_available = models.PositiveIntegerField(default=0)
    topic = models.TextField(max_length=254, default="")
    days = models.CharField(max_length=25, default="")
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    facility_description = models.TextField(max_length=254, default="")

    class Meta:
        verbose_name_plural = "courses"

    def __str__(self):
        return str(self.subject) + " " + str(self.catalog_number)

    def get_absolute_url(self):
        return reverse("home:course", kwargs={
            "pk" : self.pk
        
        })

    def get_add_to_cart_url(self) :
        return reverse("cart:add-to-cart", kwargs={
            "pk" : self.pk
        })

    def get_remove_from_cart_url(self) :
        return reverse("cart:remove-from-cart", kwargs={
            "pk" : self.pk
        })

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.course.subject}: {self.course.catalog_number}"
    
    def get_course_units(self):
        return self.course.units
