"""
just a ru_python bot
"""

import datetime
import json
import os
import sys

import telegram


def process_update(api, update):
    with open('log.txt', 'a', encoding='utf8') as log:
        json.dump(update, log, ensure_ascii=False)
        log.write('\n\n')


if __name__ == '__main__':
    token = os.environ.get('BOT_TOKEN', None)
    if not token:
        print('Please specify a BOT_TOKEN environment variable')
        sys.exit()
    api = telegram.TelegramApi(token)
    offset = 0

    while True:
        print(datetime.datetime.now(), end=' ', flush=True)
        try:
            ret = api.get_updates(offset=offset+1, timeout=30)
            if ret['ok']:
                updates = ret['result']
                print(f'Got {len(updates)} updates.')
                for update in updates:
                    offset = update['update_id']
                    process_update(api, update)
        except Exception as e:
            print(e)
