from django.db import models
from django.conf import settings

class FriendList(models.Model):
    # OneToOne = One FriendList per user and vice-versa; on_delete = delete friend list if user is deleted
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

    # ManyToMany = many users can be on the same FriendList and many FriendLists can have the same user
    # blank = user can have no friends
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    # Python refers to toString as __str__
    def __str__(self):
        return (self.user.username + ' is friends with {' + self.friends + '}')

    # params: self is a FriendList, while target is a Django User
    def add_friend(self, target):
        self.friends.add(target)

    # params: self is a FriendList, while traitor is a Django User
    def remove_friend(self, traitor):
        self.friends.remove(traitor)
        FriendList.objects.get(user=traitor).friends.remove(self.user)

    # params: self is a FriendList, while who_dis is a Django User
    def is_friend(self, who_dis):
        return who_dis in self.friends.all()


class FriendRequest(models.Model):

    '''
    Foreign Key is a One-to-Many relationship:
        A sender can send out many requests
        A request is unique to one sender
    '''
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')

    is_pending = models.BooleanField(default=True, blank=True, null=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.sender.username + ' wants to be friends with ' + self.receiver.username)

    def accept_request(self):
        sender_FL = FriendList.objects.get(user=self.sender)
        receiver_FL = FriendList.objects.get(user=self.receiver)
        if receiver_FL and sender_FL:
            receiver_FL.add_friend(self.sender)
            sender_FL.add_friend(self.receiver)
            self.is_active = False

    # This is from receiver's perspective
    def reject_request(self):
        self.is_active = False

    # This is from sender's perspective
    def cancel_request(self):
        self.is_active = False