# utilities is a "others" file where you put stuff that doesn't fit anywhere

from .models import FriendRequest
from enum import Enum

class FRIEND_REQUEST_SENT(Enum):
    REQUEST_GOT = 1
    REQUEST_NONE = 0
    REQUEST_GIVEN = -1

def get_request_status(sender, receiver):
    try:
        return FriendRequest.object.get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False