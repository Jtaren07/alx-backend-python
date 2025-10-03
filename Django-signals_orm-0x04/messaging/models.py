from django.db import models
from django.contrib.auth.models import User
from managers import UnrealMessagesManager

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = modeld.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')
    read = models.BooleanField(default=False)

    objects = models.Manager()
    unread = UnreadMessagesManager()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=False)

class MessageHistory(models.Model):
    message = models.ForeignKey(message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
