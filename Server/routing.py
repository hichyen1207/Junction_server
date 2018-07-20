from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from user.consumers import ChatConsumer, FriendListConsumer

application = ProtocolTypeRouter({

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url("^message/(?P<message_id>[^/]+)/$", ChatConsumer),
            url("^friendList/(?P<user_id>[^/]+)/$", FriendListConsumer),
        ])
    ),

})