"""
just a ru_python bot
"""

import json
import os
import sys
import logging
import logging.config
import yaml

import telegram


new_users = [] #FIXME: new_users list separated by chat
bots = [] #FIXME: persistent storage for this lists 

LOGGER = logging.getLogger('ru_telegram_bot')


def is_spam(message):
    """
    check if message is spam. TODO: think about bayes filters
    """
    text = message['text']
    LOGGER.info('Checking for spam %s', text)
    return 't.me' in text or '@' in text


def new_member(api, message):
    """
    new member event.
    """
    sender = message['new_chat_participant']
    sender_id = sender['id']
    sender_name = ' '.join((sender.get('first_name', ''), sender.get('last_name', '')))
    LOGGER.info('new member id=%s %s', sender_id, sender_name)
    new_users.append(sender['id'])


def new_message(api, message):
    """
    new message event.
    - check sender in the list of known spammers
    - in case first message from the user check it for spam
    
    TODO: several checks via 
    """
    sender_id = message['from']['id']
    if sender_id not in new_users:
        return
    if sender_id in bots:
        set_ban(api, message, reason='was bot')
    if is_spam(message):
        bots.append(sender_id)
        set_ban(api, message, reason='spam detected')
    else:
        new_users.remove(sender_id)


def set_ban(api, message, reason):
    """
    ban user in channel, forward message to the
    """
    sender = message['from']
    sender_id = sender['id']
    sender_name = ' '.join((sender.get('first_name', ''), sender.get('last_name', '')))
    chat = message['chat']
    chat_name = chat['username']

    # forward message to the special channel
    LOGGER.info('Remove message %s', message.get('text', ''))
    api.forward_message(chat_id=-1001125677827,
                        from_chat_id=message['chat']['id'], 
                        message_id=message['message_id'])
    api.send_message(chat_id=-1001125677827, text=f'Chat: {chat_name}\nSender:{sender_name} {sender_id}\n{reason}')
    # remove the message
    # ban user
    LOGGER.info('Ban user id=%s %s', sender_id, sender_name)


def process_update(api, update):
    with open('updates.txt', 'a', encoding='utf8') as log:
        json.dump(update, log, ensure_ascii=False)
        log.write('\n\n')
    message = update.get('message', {})
    if 'new_chat_participant' in message:
        new_member(api, message)
    elif 'text' in message:
        new_message(api, message)


if __name__ == '__main__':
    with open('logging.conf') as f:
        logging.config.dictConfig(yaml.load(f))

    token = os.environ.get('BOT_TOKEN', None)
    if not token:
        LOGGER.error('Please specify a BOT_TOKEN environment variable')
        sys.exit()
    api = telegram.TelegramApi(token)
    offset = 0
    LOGGER.info('Started.')

    while True:
        try:
            ret = api.get_updates(offset=offset + 1, timeout=30)
            if ret['ok']:
                updates = ret['result']
                LOGGER.debug('Got %s updates', len(updates))
                for update in updates:
                    offset = update['update_id']
                    process_update(api, update)
        except Exception as e:
            LOGGER.exception(e)
