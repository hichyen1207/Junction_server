import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, MessageContent, User
from apns2.client import APNsClient
from apns2.payload import Payload
# from Server.settings import APNS_CERT, APNS_TOPIC, USE_SANDBOX
from Server.setting.base import APNS_CERT, APNS_TOPIC, USE_SANDBOX

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.scope['message_id'] = self.scope["url_route"]["kwargs"]["message_id"]
        self.scope['room_name'] = "chatRoom_" + self.scope['message_id']
        async_to_sync(self.channel_layer.group_add)(self.scope['room_name'], self.channel_name)
        print('chat consumer websocket connect with message_id:', self.scope['message_id'])
        self.accept()

    def disconnect(self, close_code):
        print('chat consumer websocket disconnect with message_id:', self.scope['message_id'])
        async_to_sync(self.channel_layer.group_discard)(self.scope['room_name'], self.channel_name)

    def receive(self, text_data):
        # get parameter
        text_data_json = json.loads(text_data)
        self.scope['user'] = text_data_json['user_id']
        content = text_data_json['content']
        time = text_data_json['time']

        # save message to DB
        message = Message.objects.get(message_id=self.scope['message_id'])
        id = len(message.messages) + 1
        new_message_content = MessageContent(id=id, user_id=self.scope['user'], time=time, content=content)
        message.update(add_to_set__messages=new_message_content)


        # Send Push Notifications
        if message.user_id.user_1 == self.scope['user']:
            receiver_user = message.user_id.user_2
            receiver_user_notification = message.notification.user_2
        else:
            receiver_user = message.user_id.user_1
            receiver_user_notification = message.notification.user_1
        send_user = User.objects.get(user_id=self.scope['user'])
        receiver_user = User.objects.get(user_id=receiver_user)
        receiver_user_ios_device_id = receiver_user.device.ios
        try:
            if receiver_user_ios_device_id != '' and receiver_user_notification:
                notification_content = send_user.english_name + ': ' + content
                custom_payload = {
                    'type': 'message',
                    'message_id': self.scope['message_id'],
                    'user_id': send_user.user_id,
                    'english_name': send_user.english_name,
                    'chinese_name': send_user.chinese_name,
                    'photo': send_user.photo
                }
                payload = Payload(alert=notification_content, sound="default", badge=1, custom=custom_payload)
                client = APNsClient(APNS_CERT, use_sandbox=USE_SANDBOX, use_alternative_port=False)
                client.send_notification(receiver_user_ios_device_id, payload, APNS_TOPIC)
        except Exception as e:
            print(e)

        # Send WebSocket
        async_to_sync(self.channel_layer.group_send)(
            self.scope['room_name'],
            {
                "type": "chat.message",
                "text": json.dumps({
                    "content_id": id,
                    "user_id": self.scope['user'],
                    "time": time,
                    "content": content,
                }),
            },
        )

    def chat_message(self, event):
        self.send(text_data=event["text"])

class FriendListConsumer(WebsocketConsumer):
    def connect(self):
        self.scope['user_id'] = self.scope["url_route"]["kwargs"]["user_id"]
        self.scope['room_name'] = "friendList_" + self.scope['user_id']
        async_to_sync(self.channel_layer.group_add)(self.scope['room_name'], self.channel_name)
        print('chat room consumer websocket connect with user_id:', self.scope['user_id'])
        self.accept()

    def disconnect(self, close_code):
        print('chat room consumer websocket disconnect with user_id:', self.scope['user_id'])
        async_to_sync(self.channel_layer.group_discard)(self.scope['room_name'], self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id = text_data_json['user_id']
        time = text_data_json['time']
        message_id = text_data_json['message_id']

        message = Message.objects.get(message_id=message_id)
        total_message = len(message.messages)
        unread_message_number = 1
        if message.user_id.user_1 == sender_id:
            last_read_message = message.last_read_message.user_1
        else:
            last_read_message = message.last_read_message.user_2

        for message_index in range(last_read_message, total_message):
            if message.messages[message_index].user_id == sender_id and message.messages[
                message_index].is_read == False:
                unread_message_number += 1

        async_to_sync(self.channel_layer.group_send)(
            self.scope['room_name'],
            {
                "type": "chat.message",
                "text": json.dumps({
                    "message_id": message_id,
                    "time": time,
                    "unread_message_number": unread_message_number,
                }),
            },
        )

    def chat_message(self, event):
        self.send(text_data=event["text"])