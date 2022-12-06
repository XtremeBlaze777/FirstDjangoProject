from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from friends.models import FriendList

@login_required
def index(request):
    curUser = User.objects.get(username=request.user)

    object_list = []
    list_of_friend_list = FriendList.objects.filter(user=curUser)
    for fl in list_of_friend_list:
        for f in fl.friends.all():
            object_list.append(f)

    return render(request, 'profile.html', { 'object_list' : object_list, 'curUser' : curUser })
