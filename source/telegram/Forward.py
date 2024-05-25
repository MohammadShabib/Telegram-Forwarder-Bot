import os

from telethon import events

from source.model.History import History
from source.utils.Constants import MEDIA_FOLDER_PATH


class Forward:
    def __init__(self, client, forward_config_map):
        self.client = client
        self.forward_config_map = forward_config_map
        self.history = History()

    def add_events(self):
        self.client.add_event_handler(self.message_handler,
                                      events.NewMessage(chats=list(self.forward_config_map.keys())))
        self.client.add_event_handler(self.album_handler, events.Album(chats=list(self.forward_config_map.keys())))

    async def message_handler(self, event):
        try:
            if event.grouped_id:
                return
            destination_id = self.forward_config_map.get(event.chat_id).destinationID
            reply_message = await self.reply_handler(event.message, destination_id)
            await self.send_message(destination_id, event.message, reply_to=reply_message)
        except Exception as e:
            print(e)

    async def album_handler(self, event):
        try:
            destination_id = self.forward_config_map.get(event.chat_id).destinationID
            reply_message = None
            for message in event.messages:
                temp = await self.reply_handler(message, destination_id)
                if not temp is None:
                    reply_message = temp
            await self.send_album(destination_id, event, reply_to=reply_message)
        except Exception as e:
            print(e)

    async def forward_all_history(self):
        last_message_id = 0
        for source in self.forward_config_map:
            messages = await self.client.get_messages(source, min_id=last_message_id, limit=None)
            for message in reversed(messages):
                destination_id = self.forward_config_map.get(message.chat_id).destinationID
                reply_message = await self.reply_handler(message, destination_id)
                await self.send_message(destination_id, message, reply_to=reply_message)
                last_message_id = max(last_message_id, message.id)
        self.client.disconnect()

    async def reply_handler(self, source_message, destination_id):
        if not source_message.is_reply:
            return None
        return self.history.get_mapping(source_message.chat_id, source_message.reply_to_msg_id, destination_id)
        # replied_message = \
        #     (await self.client.get_messages(source_message.chat_id, ids=[source_message.reply_to_msg_id]))[0]
        # replied_message.text = replied_message.text + "```This message was previously sent and is being resent for a reply purpose only```"
        # replied_message_sent = await self.send_message(destination_id, replied_message)
        # return replied_message_sent.id

    async def send_message(self, destination_channel_id, message, reply_to=None):
        try:
            lSent_message = None
            media_path = None
            if message.media:
                media_path = await self.download_media(message)
            text = message.text if message.text else ''
            if media_path:
                lSent_message = await self.client.send_file(destination_channel_id, media_path, caption=text,
                                                            reply_to=reply_to)
                self.delete_media(media_path)
            else:
                lSent_message = await self.client.send_message(destination_channel_id, text, reply_to=reply_to)
            self.history.add_mapping(message.chat_id, message.id, lSent_message.chat_id, lSent_message.id)
            return lSent_message
        except Exception as err:
            print(err)
            return None

    async def send_album(self, destination_channel_id, event, reply_to=None):
        # TODO: ADD compression flag
        media_path_list = []
        for message in event.messages:
            if message.media:
                media_path = await self.download_media(message)
                media_path_list.append(media_path)
        lSent_message = await self.client.send_file(destination_channel_id, media_path_list, caption=event.text,
                                                    reply_to=reply_to)
        for i in range(0, len(event.messages)):
            self.history.add_mapping(event.chat_id, event.messages[i].id, destination_channel_id, lSent_message[i].id)

        for media_path in media_path_list:
            self.delete_media(media_path)

    async def download_media(self, message):
        if not os.path.exists(MEDIA_FOLDER_PATH):
            os.makedirs(MEDIA_FOLDER_PATH)

        file_path = await self.client.download_media(message, file=MEDIA_FOLDER_PATH)
        return file_path

    @staticmethod
    def delete_media(media_path):
        os.remove(media_path)
