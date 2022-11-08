from django.contrib.auth.models import User
from .views import *

class user(User):
    def make_friend_request(self):
        