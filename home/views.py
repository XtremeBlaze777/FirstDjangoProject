from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView, View
from .models import *
import requests
import numpy as np
import pandas as pd


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            cart = Cart.objects.get(user=self.request.user)
            context = {
                'object' : cart
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have a cart")
            return redirect("/")

@login_required
def add_to_cart(request, pk) :
    course = get_object_or_404(Course, pk = pk )
    cart_item, created = CartItem.objects.get_or_create(
        course=course,
        user = request.user
    )
    cart_qs = Cart.objects.filter(user=request.user)

    if cart_qs.exists() :
        cart = cart_qs[0]
        if cart.courses.filter(course__pk = course.pk).exists() :
            cart_item.save()
            print("ADDED ITEM TO CART")
            messages.info(request, "Added Course")
            return redirect("home:cart-summary")
        else:
            print("ADDED ITEM TO CART")
            cart.courses.add(cart_item)
            messages.info(request, "Course added to your cart")
            return redirect("home:cart-summary")
    else:
        cart = Cart.objects.create(user=request.user)
        cart.courses.add(cart_item)
        print("CREATED CART AND ADDED ITEM")
        messages.info(request, "Course added to your cart")
        return redirect("home:cart-summary")

@login_required
def remove_from_cart(request, pk):
    course = get_object_or_404(Course, pk=pk )
    cart_qs = Cart.objects.filter(
        user=request.user, 
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.courses.filter(course__pk=course.pk).exists():
            cart_item = CartItem.objects.filter(
                course=course,
                user=request.user
            )[0]
            cart_item.delete()
            print("ITEM REMOVED")
            messages.info(request, "Course \""+ cart_item.course.subject + ": " + cart_item.course.catalog_number +"\" removed from your cart")
            return redirect("home:cart-summary")
        else:
            print("WHY AM I HERE??????")
            messages.info(request, "This Course is not in your cart")
            return redirect("home:course_description", pk=pk)
    else:
        print("WHY AM I HERE")
        messages.info(request, "You do not have a cart")
        return redirect("home:course_description", pk = pk)



class HomeView(TemplateView):
    template_name = "home.html"

class SearchResultsView(ListView):
    model = Course
    template_name = "course.html"

    def get_queryset(self):  
        query = self.request.GET.get("q")
        object_list = Course.objects.filter(
            Q(subject__icontains=query)
        )
        return object_list

class CourseDescriptionView(DetailView):
    model = Course
    template_name = "section.html"


################# BELOW IS NOT USED ################################
def home(request, subject):
    course = get_object_or_404(Course, pk=subject)
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
        return HttpResponseRedirect('/subject/' + subject + "/course/" + str(courseNum) + "/section/" + sectionNum + "/")
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
    description = info['description']
    return render(request, 'section.html',{'description' : description, 'courseName' : courseName, 'sectionNum' : sectionNum,
                                           'name' : name, 'email' : email, 'courseNum' : courseNum, 'capacity' : capacity, 'waitList' : waitList,
                                               'waitListCap' : waitListCap, 'spotsTaken' : spotsTaken, 'spotsOpen' : spotsOpen,'day' : day, 'startTime' : startTime,
                                                   'endTime' : endTime,'location' : location,'response':response})
