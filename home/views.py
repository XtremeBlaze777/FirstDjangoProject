from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests
import numpy as np
import pandas as pd

def index(request):
    return HttpResponse("Hello, world. You're at the home page for Team A-8's new LousList.")

def home(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        request.session['subject'] = subject
        return HttpResponseRedirect('/subject/' + subject)
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist?format=json').json()
    return render(request, 'home.html',{'response':response})

    
def subject(request,subject):
    if request.method == 'POST':
        courseNum = request.POST.get('class')
        return HttpResponseRedirect('/subject/' + subject + "/course/" + courseNum)
    response = requests.get('http://luthers-list.herokuapp.com/api/dept/' + subject + '/?format=json').json()
    df = pd.DataFrame.transpose(pd.DataFrame.from_dict(response))
    courses = df.loc['description'].unique()
    courseNums = df.loc['catalog_number'].unique()
    courseNums = courseNums
    return render(request, 'classes.html',{'Info': zip(courses,courseNums),'response':response})

def course(request,subject,courseNum):
    response = requests.get('http://luthers-list.herokuapp.com/api/dept/' + subject + '/?format=json').json()
    df = pd.DataFrame.transpose(pd.DataFrame.from_dict(response))
    indices = df.loc['catalog_number'] == str(courseNum)
    df = pd.DataFrame.transpose(df.loc[:,indices])
    courseName = subject + str(courseNum)
    
    instructorNames = df['instructor'].apply(lambda x: x['name'])
    spots = df['enrollment_available']
    classTimes = df['meetings'].apply(lambda x: x[0]['days'])

    return render(request, 'course.html',{'courseName' : courseName, 'Info': zip(instructorNames,spots,classTimes),'response':response})
