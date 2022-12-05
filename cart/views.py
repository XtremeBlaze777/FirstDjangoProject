from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from schedule.models import Schedule, Comment
import numpy as np
import pandas as pd
import requests
from .models import *

# Create your views here.

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
            return redirect("cart:cart-summary")
        else:
            print("ADDED ITEM TO CART")
            cart.courses.add(cart_item)
            messages.info(request, "Course added to your cart")
            return redirect("cart:cart-summary")
    else:
        cart = Cart.objects.create(user=request.user)
        cart.courses.add(cart_item)
        print("CREATED CART AND ADDED ITEM")
        messages.info(request, "Course added to your cart")
        return redirect("cart:cart-summary")

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
            return redirect("cart:cart-summary")
        else:
            print("WHY AM I HERE??????")
            messages.info(request, "This Course is not in your cart")
            return redirect("cart:course_description", pk=pk)
    else:
        print("WHY AM I HERE")
        messages.info(request, "You do not have a cart")
        return redirect("cart:course_description", pk = pk)

@login_required
def create_schedule(request):
    Schedule.objects.filter(user=request.user).delete()
    cart = Cart.objects.filter(
        user=request.user, 
    )
    schedule, created = Schedule.objects.get_or_create(
        user = request.user,
        pub_date = timezone.now()
    )
    cart_qs = Cart.objects.filter(user=request.user)
    cart = cart_qs[0]
    if cart.courses.count != 0:            
        for course in cart.courses.all():
            schedule.courses.add(course.course)
        
        print("CREATED SCHEDULE: ")
        messages.info(request, "Schedule created")
        return redirect("schedule:schedule_view")
    else:
        print("NO COURSES TO SCHEDULE")
        messages.info(request, "Cannot create schedule without courses")
    
class SearchResultsView(ListView):
    model = Course
    template_name = "course.html"

    def get_queryset(self):  
        if 'q' in self.request.GET:
            query = self.request.GET.get("q")
            object_list = Course.objects.filter(
                Q(subject__icontains=query)
            )
            return object_list
        if 't' in self.request.GET:
            query = self.request.GET.get("t")
            object_list = Course.objects.filter(
                Q(instructor_name__icontains=query)
            )
            return object_list
        if 'u' in self.request.GET:
            print("test")
            query = self.request.GET.get("u")
            courseSubject  = query.rstrip('0123456789')
            print(courseSubject)
            courseCode = query[len(courseSubject):]
            print(courseCode)
            object_list = Course.objects.filter(
                Q(subject__icontains=courseSubject)
            )
            object_list = object_list.filter(
                Q(catalog_number__icontains=courseCode)
            )
            return object_list
        if 'v' in self.request.GET:
            query = self.request.GET.get("v")
            object_list = Course.objects.filter(
                Q(course_number__icontains=query)
            )
            return object_list

class CourseDescriptionView(DetailView):
    model = Course
    template_name = "section.html"
