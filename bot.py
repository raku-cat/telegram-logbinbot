#!/usr/bin/env python3
import telepot, telepot.aio
import os
import sys
import json
import requests
import regex
import asyncio, aiohttp
from telepot.aio.loop import MessageLoop

with open(sys.path[0] + '/keys.json', 'r') as f:
    key = json.load(f)
bot = telepot.aio.Bot(key['telegram'])

async def on_command(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
    #print(msg)
    try:
        if regex.match(r'(^».\[.*\..*\..*\]\:.*)', msg['text']) is not None and len(msg['text'].split('\n')) > 5 or msg['text'].startswith('Build version:'):
            paste = {'c': msg['text']}
            await bot.sendChatAction(chat_id, 'typing')
            async with aiohttp.ClientSession() as session:
                async with session.post('https://ptpb.pw/?u=1', json=paste) as resp:
                    if resp.status == 200:
                        messageid = telepot.message_identifier(msg)
                        pastedlog = await resp.text()
                        try:
                            fname = msg['from']['first_name'] + ' ' + msg['from']['last_name']
                        except KeyError:
                            fname = msg['from']['first_name']
                        await bot.sendMessage(chat_id, '[' + fname + '](tg://user?id=' + str(msg['from']['id']) + '):\n' + pastedlog, reply_to_message_id=msg_id, parse_mode='markdown')
                        try:
                            await bot.deleteMessage(messageid)
                        except telepot.exception.TelegramError:
                            pass
    except KeyError:
        return

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot,{'chat' : on_command }).run_forever())
print('Started...')
loop.run_forever()
