from django.contrib import admin
from .models import *

class FL_Admin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList

class Request_Admin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender', 'receiver']

    class Meta:
        model = FriendRequest

admin.site.register(FriendList, FL_Admin)
admin.site.register(FriendRequest, Request_Admin)
