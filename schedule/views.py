from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
import requests
from .models import *
from .forms import *

# Create your views here.
class ScheduleView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            schedule = Schedule.objects.get(user=self.request.user)
            context = {
                'object' : schedule
            }
            return render(self.request, 'schedule.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have a schedule")
            return redirect("/")



def schedule_view(request):
    try:
        schedule = Schedule.objects.get(user=request.user.id)
        comments = schedule.comments.filter(status=True)
        user_comment = None
        if request.method == 'POST':
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.schedule = schedule
                user_comment.save()
                #return HttpResponseRedirect("/")
        else:
            comment_form = NewCommentForm()
        return render(
            request, 'schedule.html', {
                'schedule' : schedule, 
                'comments' : user_comment, 
                'comments' : comments, 
                'comment_form' : comment_form},)
    except ObjectDoesNotExist:
        messages.error(request, "Schedule is not available")
        return redirect("/")

def friend_schedule_view(request, user_id):
    try:
        schedule = Schedule.objects.get(user=user_id)
        comments = schedule.comments.filter(status=True)
        user_comment = None
        if request.method == 'POST':
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.schedule = schedule
                user_comment.save()
                #return HttpResponseRedirect("/")
        else:
            comment_form = NewCommentForm()
        return render(
            request, 'schedule.html', {
                'schedule' : schedule, 
                'comments' : user_comment, 
                'comments' : comments, 
                'comment_form' : comment_form},)
    except ObjectDoesNotExist:
        messages.error(request, "Friend's schedule is not available")
        return redirect("/")

    
    