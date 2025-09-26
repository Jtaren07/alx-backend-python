from rest_framework import viewsets, status, filters #type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from models import Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import HTTP_403_FORBIDDEN


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        
    #def get_queryset(self):
    #   # Show only conversations the user participates in
    #    return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.query_params.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(conversation_id=Conversation_id)
        return Message.objects.filter()

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant of this conversation.",
                             },
                            status=HTTP_403_FORBIDDEN
                             )
        serializer.save(sender=self.request.user)

