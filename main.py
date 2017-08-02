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


LOGGER = logging.getLogger('ru_telegram_bot')


def process_update(api, update):
    with open('updates.txt', 'a', encoding='utf8') as log:
        json.dump(update, log, ensure_ascii=False)
        log.write('\n\n')


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
            ret = api.get_updates(offset=offset+1, timeout=30)
            if ret['ok']:
                updates = ret['result']
                LOGGER.debug('Got %s updates', len(updates))
                for update in updates:
                    offset = update['update_id']
                    process_update(api, update)
        except Exception as e:
            LOGGER.exception(e)
