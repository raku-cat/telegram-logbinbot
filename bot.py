#!/usr/bin/env python3
import telepot, telepot.aio
import os
import sys
import json
import requests
import asyncio, aiohttp
from telepot.aio.loop import MessageLoop

with open(sys.path[0] + '/keys.json', 'r') as f:
    key = json.load(f)
bot = telepot.aio.Bot(key['telegram'])

async def on_command(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
#    print(msg['text'])
    try:
        if 'Build version:' in msg['text']:
            paste = {'c': msg['text']}
            await bot.sendChatAction(chat_id, 'typing')
            async with aiohttp.ClientSession() as session:
                async with session.post('https://ptpb.pw/?u=1', json=paste) as resp:
                    if resp.status == 200:
                        messageid = telepot.message_identifier(msg)
                        pastedlog = await resp.text()
                        await bot.sendMessage(chat_id, pastedlog, reply_to_message_id=msg_id)
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