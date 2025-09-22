# permissions.py
from rest_framework.permissions import BasePermission
from .models import Conversation

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to check if the user is a participant of the conversation.
    """

    def has_permission(self, request, view):
        # Allow read-only access for anyone (e.g., to list conversations)
        if view.action in ['list', 'retrieve', 'create']:
            return request.user.is_authenticated

        # For other actions like 'update', 'destroy', we need to check object-level permissions
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation object.
        # This handles access to individual Conversation or Message objects.
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        
        # If the object is a Message, check the parent conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
            
        return False
