import requests
from django.core.management.base import BaseCommand
import pandas as pd
from ...models import Department, Course

def get_subjects():
  url = 'http://luthers-list.herokuapp.com/api/deptlist'
  r = requests.get(url, headers={'Content-Type':      
    'application/json'})
  subject = r.json()
  return subject

def seed_subject():
  for i in get_subjects():
    seed_courses(i['subject'])
    

def get_courses(subject):
  url = 'http://luthers-list.herokuapp.com/api/dept/' + subject
  r = requests.get(url, headers={'Content-Type':      
    'application/json'})
  course = r.json()
  return course

def seed_courses(subject):
  for i in get_courses(subject):
    course = Course(
        instructor_name = i['instructor']['name'],
        instructor_email = i['instructor']['email'],
        course_number = i['course_number'],
        course_section = i['course_section'],
        subject = i['subject'],
        catalog_number = i['catalog_number'],
        description=i['description'],
        units = i['units'],
        component = i['component'],
        class_capacity = i['class_capacity'],
        wait_list = i['wait_list'],
        wait_cap = i['wait_cap'],
        enrollment_total = i['enrollment_total'],
        enrollment_available = i['enrollment_available'],
        topic = i['topic'],
    )
    if len(i['meetings']) != 0:
        if i['meetings'][0]['start_time'] == "":
            curr_start = "0.0.0.0-00:00"
            curr_end = "0.0.0.0-00:00"
        else:
            curr_start = i['meetings'][0]['start_time']
            curr_end = i['meetings'][0]['end_time']
        course.days = i['meetings'][0]['days']
        course.start_time = pd.to_datetime(curr_start.replace(":",""), format = "%H.%M.%S.%f%z")
        course.end_time = pd.to_datetime(curr_end.replace(":",""), format = "%H.%M.%S.%f%z")
        course.facility_description = i['meetings'][0]['facility_description']
    course.save()



def clear_data():
  Course.objects.all().delete()

class Command(BaseCommand):
  def handle(self, *args, **options):
    clear_data()
    seed_subject()
    print("completed populating database with courses")