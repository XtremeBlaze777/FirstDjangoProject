from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    return HttpResponse("Hello, world. You're at the home page for Team A-8's new LousList.")

def home(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist?format=json').json()
    if request.method == 'POST':
        subject = request.POST.get('subject')
        print(subject)
        print("---------------\n\n")
        response = requests.get('http://luthers-list.herokuapp.com/api/dept/' + subject + '/?format=json').json()
        return render(request, 'classes.html',{'response':response})
    return render(request, 'home.html',{'response':response})
