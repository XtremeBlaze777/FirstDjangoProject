from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class FriendList(models.Model):
    # OneToOne = One FriendList per user and vice-versa; on_delete = delete friend list if user is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')

    ''' ManyToMany = many users can be on the same FriendList and many FriendLists can have the same user
        blank = user can have no friends '''
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    schedules = models.ManyToManyField
    # Python refers to toString as __str__
    def __str__(self):
        return (self.user.username + '\'s friend list')

    # params: self is a FriendList, while target is a Django User
    def add_friend(self, target):
        self.friends.add(target)
        self.save()

    # params: self is a FriendList, while traitor is a Django User
    def remove_friend(self, traitor):
        self.friends.remove(traitor)
        FriendList.objects.get(user=traitor).friends.remove(self.user)
        self.save()

    # params: self is a FriendList, while who_dis is a Django User
    def is_friend(self, who_dis):
        return who_dis in self.friends.all()


class FriendRequest(models.Model):

    '''
    Foreign Key is a One-to-Many relationship:
        A sender can send out many requests
        A request is unique to one sender
    '''
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    time_stamp = models.DateTimeField(auto_now_add=True)
    is_pending = models.BooleanField(default=True, blank=True, null=False)

    def __str__(self):
        return ('Sent a friend request to ' + self.receiver.username)

    def accept_request(self):
        sender_FL = None
        receiver_FL = None
        try:
            sender_FL = FriendList.objects.get(user=self.sender)
        except:
            sender_FL = FriendList.objects.create(user=self.sender)
        try:
            receiver_FL = FriendList.objects.get(user=self.receiver)
        except:
            receiver_FL = FriendList.objects.create(user=self.receiver)
            
        if self.is_pending != False:
            receiver_FL.add_friend(self.sender)
            sender_FL.add_friend(self.receiver)
            self.is_pending = False
            self.save()

    # This is from receiver's perspective
    def reject_request(self):
        self.is_pending = False
        self.save()

    # This is from sender's perspective
    def cancel_request(self):
        self.is_pending = False
        self.save()