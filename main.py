"""
just a ru_python bot
"""

import datetime
import json
import os
import sys

import telegram


token = os.environ.get('BOT_TOKEN', None)
if not token:
    print('Please specify a BOT_TOKEN environment variable')
    sys.exit()
api = telegram.TelegramApi(token)
offset = 0

log = open('log.txt', 'a', encoding='utf8')

while True:
    print(datetime.datetime.now(), end=' ', flush=True)
    try:
        ret = api.get_updates(offset=offset+1, timeout=30)
        if ret['ok']:
            updates = ret['result']
            print(f'Got {len(updates)} updates.')
            for update in updates:
                offset = update['update_id']
                log.write(json.dumps(update, ensure_ascii=False))
                log.write('\n\n')
                log.flush()
    except Exception as e:
        print(e)
