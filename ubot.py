# Import Library
import time
import gc
import ujson
import urequests
import wifi


class ubot:
    
    def __init__(self, token, offset=0):
        """
        Initialize the bot object with the given token and the offset
        """
        self.url = 'https://api.telegram.org/bot' + token
        self.commands = {}
        self.default_handler = None
        self.message_offset = offset
        self.sleep_btw_updates = 3 # sleep time in seconds between updates
 
    def read_once(self):
        """
        Read incoming messages and handle them
        """
        messages = self.read_messages()
        print('Bot read message')
        if messages:
            # Check if the message offset is 0, if yes set it to the next message's update_id
            if self.message_offset == 0:
                # The offset is placed on the next message
                # Offset will be update id of the next message
                self.message_offset = messages[-1]['update_id']
                # next message will be processed
                part = self.message_handler(messages[-1])
            else:
                # If the message offset is not 0, check all messages received
                for message in messages:
                    # If the message update_id is greater or equal to the message offset, process it
                    if message['update_id'] >= self.message_offset:
                        self.message_offset = message['update_id']
                        part = self.message_handler(message)
        else:
            print('There are no new messages')
                    
    

    def read_messages(self):
        """
        Read incoming messages using Telegram Bot API
        """
        query_updates = {
            'offset': self.message_offset +1,
            'limit': 1,
            'timeout': 0.01,
            'allowed_updates': ['message']}
        try:
            # Check if the device is connected to Wi-Fi
            if wifi.is_connected():
                # Send request to Telegram Bot API to get updates
                response = urequests.get(self.url + '/getUpdates', json=query_updates)
                # Extract messages from the response
                return response.json()['result']
        except:
            pass
    
    def message_handler(self, message):
        """
        Handling incoming messages from Telegram
        """
        # Check if the message has text and does not contain any media types (photo, document, audio, voice, video)
        if 'text' in message['message'] and not any(key in message['message'] for key in ['photo', 'document', 'audio', 'voice', 'video']):
            # Check if the message has text
            if 'text' in message['message']:
                # Split the message into parts, separated by spaces
                parts = message['message']['text'].split(' ')
                # Check each part of the message text for a command
                for part in parts :
                    if part in self.commands:
                        # If the part is a command, call the corresponding command handler
                        print('got command: ', part)
                        # hier beginnt die AKTION-PHASE
                        self.commands[part](message)
                        # hier Endet die AKTION-PHASE
                    else:
                        # If the part is not a command, call the default handler
                        print('got text: ', part)
                        self.default_handler(message)
        else:
            # If the message is not just text or contains media types, call the default handler
            print('message contains not only text')
            self.default_handler(message)
    
    
    def register(self, command, handler):
        """
        Register a command with a corresponding handler function
        
        .. note::
            The register method takes two arguments: a string command and a handler function
            that should be called when the specified command is received by the bot.
            The method adds the command and its associated handler to the bot's commands dictionary.
        """
        self.commands[command] = handler

    def set_default_handler(self, handler):
        """
        Set a default handler for when no command is matched
        
        .. note::
            The set_default_handler method takes a single argument: a default handler function
            that will be called when the bot receives a message that does not match any registered commands.
        """
        self.default_handler = handler
        

    def send(self, chat_id, text):
        """
        Send a message to a chat with the given chat ID and text content
        """
        # Construct a dictionary of query parameters to be sent with the HTTP POST request
        query_updates = {
            'chat_id': chat_id,
            'text': text,
            'timeout': 0.01,
            'parse_mode': 'HTML'}
        # Define headers for the HTTP request
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}
        try:
            # Check if the device is connected to Wi-Fi
            if wifi.is_connected():
                # Send an HTTP POST request to the Telegram API with the message content and headers
                response = urequests.post(self.url + '/sendMessage', json=query_updates, headers=headers)
                response.close()
        except:
            pass        
    
    def reply_to(self, chat_id, text, reply_to_message_id=None):
        """
        Reply to a specific message in a chat with the given chat ID, text content,
        and message ID to reply to (optional)
        """
        # Construct a dictionary of query parameters to be sent with the HTTP POST request
        query_updates = {
            'chat_id': chat_id,
            'text': text,
            'timeout': 0.01,
            'parse_mode': 'HTML',
            'reply_to_message_id': reply_to_message_id}
        # Define headers for the HTTP request
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}
        try:
            # Check if the device is connected to Wi-Fi
            if wifi.is_connected():
                # Send an HTTP POST request to the Telegram API with the message content and headers
                response = urequests.post(self.url + '/sendMessage', json=query_updates, headers=headers)
                response.close()
        except:
            pass
                