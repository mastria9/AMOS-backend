from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.mixins import AuthorizationMixin
from .models import Message,InboxMessage,OutboxMessage
from rest_framework import serializers




class InboxMessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InboxMessage
        fields = ('id','text','address')
        read_only_fields =('id','text','address')


class OutboxMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutboxMessage
        fields = ('id','text','address')
        read_only_fields =('id','text','address')

class MessageSerializer(serializers.ModelSerializer):
    inbox=InboxMessageSerializer(many=True)
    outbox=OutboxMessageSerializer(many=True)
    class Meta:
        model = OutboxMessage
        fields = '__all__'
        read_only_fields =('id','company','marketplace','inbox','outbox')


class MessageViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("messages")
        return queryset.order_by("id")

class MessageViewSet(MessageViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Message
    permission_classes = IsAuthenticated
    serializer_class = MessageSerializer


message_list = MessageViewSet.as_view({'get':'list','post':'create'})
message_detail = MessageViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

