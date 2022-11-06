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
    if request.method == 'POST':
        sectionNum = request.POST.get('section')
        return HttpResponseRedirect('/subject/' + subject + "/course/" + str(courseNum) + "/section/" + sectionNum)
    response = requests.get('http://luthers-list.herokuapp.com/api/dept/' + subject + '/?format=json').json()
    df = pd.DataFrame.transpose(pd.DataFrame.from_dict(response))
    indices = df.loc['catalog_number'] == str(courseNum)
    df = pd.DataFrame.transpose(df.loc[:,indices])
    courseName = subject + str(courseNum)
    
    instructorNames = df['instructor'].apply(lambda x: x['name'])
    spots = df['enrollment_available']
    classTimes = df['meetings'].apply(lambda x: x[0]['days'])
    sectionNum = df['course_section']
    component = df['component']
    
    subject = subject
    units = df.loc[0,'units']
    description = df.loc[0,'description']

    return render(request, 'course.html',{'description' : description, 'courseName' : courseName, 'units' : units, 'Info': zip(instructorNames,spots,classTimes,sectionNum,component),'response':response})

def section(request,subject,courseNum,sectionNum):
    response = requests.get('http://luthers-list.herokuapp.com/api/dept/' + subject + '/?format=json').json()
    df = pd.DataFrame.transpose(pd.DataFrame.from_dict(response))
    indices = df.loc['catalog_number'] == str(courseNum)
    df = df.loc[:,indices]
    indices = df.loc['course_section'] == sectionNum
    df = pd.DataFrame.transpose(df.loc[:,indices])
    info = df.to_dict()
    courseName = subject + str(courseNum)

    print(info['meetings'])
    print(info['meetings'][0][0]['days'])
    name = info['instructor'][0]['name']
    email = info['instructor'][0]['email']
    courseNum = info['course_number'][0]
    
    capacity = info['class_capacity'][0]
    waitList = info['wait_list'][0]
    waitListCap = info['wait_cap'][0]
    spotsTaken = info['enrollment_total'][0]
    spotsOpen = info['enrollment_available'][0]
    day = info['meetings'][0][0]['days']
    startTime = pd.to_datetime(info['meetings'][0][0]['start_time'].replace(":",""), format = "%H.%M.%S.%f%z")
    startTime = startTime.strftime('%H:%M')
    endTime = pd.to_datetime(info['meetings'][0][0]['end_time'].replace(":",""), format = "%H.%M.%S.%f%z")
    endTime = endTime.strftime('%H:%M')
    location = info['meetings'][0][0]['facility_description']
    print(location)
    description = info['description']
    
    return render(request, 'section.html',{'description' : description, 'courseName' : courseName, 'sectionNum' : sectionNum,
                                           'name' : name, 'email' : email, 'courseNum' : courseNum, 'capacity' : capacity, 'waitList' : waitList,
                                               'waitListCap' : waitListCap, 'spotsTaken' : spotsTaken, 'spotsOpen' : spotsOpen,'day' : day, 'startTime' : startTime,
                                                   'endTime' : endTime,'location' : location,'response':response})
