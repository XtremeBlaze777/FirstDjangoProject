from django.db import models

# Create your models here.
class Department(models.Model):
    deptJson = models.JSONField(default=dict)

class CourseDescription(models.Model):
    instructor_name = models.CharField(max_length = 150)
    instructor_email = models.EmailField(max_length=254)
    course_number = models.PositiveIntegerField()
    course_subject = models.CharField(max_length = 5)
    course_title = models.TextField(max_length=254)
    course_units = models.PositiveIntegerField()

    def __str__(self):
        return self.course_title

#class Subject(models.Model):
    #courses = ArrayField(models.CharField(max_length=100), size=200)
    
    
