import os

from telethon import events

from source.utils.Constants import MEDIA_FOLDER_PATH


class Forward:
    def __init__(self, client, forward_config_map):
        self.client = client
        self.forward_config_map = forward_config_map
        self.client.add_event_handler(self.message_handler, events.NewMessage(chats=list(forward_config_map.keys())))
        self.client.add_event_handler(self.album_handler, events.Album(chats=list(forward_config_map.keys())))

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
            reply_message = await self.reply_handler(event.message, destination_id)
            await self.send_album(destination_id, event, reply_to=reply_message)
        except Exception as e:
            print(e)

    async def reply_handler(self, source_message, destination_id):
        if not source_message.is_reply:
            return None
        replied_message = \
            (await self.client.get_messages(source_message.chat_id, ids=[source_message.reply_to_msg_id]))[0]
        replied_message.text = replied_message.text + "```This message was previously sent and is being resent for a reply purpose only```"
        replied_message_sent = await self.send_message(destination_id, replied_message)
        return replied_message_sent.id

    async def send_message(self, destination_channel_id, message, reply_to=None):
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
        return lSent_message

    async def send_album(self, destination_channel_id, event, reply_to=None):
        # TODO: ADD compression flag
        media_path_list = []
        for message in event.messages:
            if message.media:
                media_path = await self.download_media(message)
                media_path_list.append(media_path)
        await self.client.send_file(destination_channel_id, media_path_list, caption=event.text, reply_to=reply_to)
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
