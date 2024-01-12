from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        self.team_id = self.scope["url_route"]["kwargs"]["team_id"]
        self.team_group_name = f"chat_{self.team_id}"
        await self.channel_layer.group_add(self.team_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                self.team_group_name, self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender, message = (
            text_data_json["sender"],
            text_data_json["message"],
        )
        created_message = await self.save_message(self.team_id, message)
        await self.channel_layer.group_send(
            self.team_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
                "timestamp": created_message.timestamp.isoformat(),
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, team_id, message):
        from teams.models import GroupMessage

        return GroupMessage.objects.create(
            team_id=team_id, text=message, user=self.scope["user"]
        )


class TeamExpensesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        self.team_id = self.scope["url_route"]["kwargs"]["team_id"]
        self.team_group_name = f"team_expenses_{self.team_id}"
        await self.channel_layer.group_add(self.team_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                self.team_group_name, self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json["sender"]
        await self.channel_layer.group_send(
            self.team_group_name,
            {
                "type": "team_expenses_message",
                "sender": sender,
            },
        )

    async def team_expenses_message(self, event):
        await self.send(text_data=json.dumps(event))
