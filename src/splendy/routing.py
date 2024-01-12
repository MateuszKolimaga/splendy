from django.urls import re_path

from teams import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<team_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(
        r"ws/team_expenses/(?P<team_id>\w+)/$", consumers.TeamExpensesConsumer.as_asgi()
    ),
]
