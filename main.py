from telethon import TelegramClient, sync, events
from telethon.sessions import StringSession

import config
import asyncio
import logging

client = TelegramClient(StringSession(
    config.session_name), config.api_id, config.api_hash)
logging.basicConfig(level=logging.INFO, filename='log.txt', format='%(asctime)s %(levelname)s:%(message)s')

flagCheck = True
flagError = True
errMessage = 0

@client.on(events.NewMessage(chats=config.source_group))
async def message_handler(event):
    global flagCheck, flagError, errMessage
    if event.message.is_reply:
        await client.delete_messages(config.source_group, [event.message.reply_to_msg_id, event.message.id])
        flagCheck, flagError = True, True
        if errMessage:
            await client.delete_messages(config.main_group, errMessage.id)
            await client.send_message(config.main_group, "SERVER STATUS ONLINE🟢")
            logging.info("check Coin scalper Bot (online again)")
            errMessage = 0
        logging.info("check Coin scalper Bot (OK)")

async def main():
    global flagCheck, flagError, errMessage
    res = None
    while True:
        if flagCheck:
            flagCheck = False
            res = await client.send_message(config.source_group, "!server status")
            logging.info("check Coin scalper Bot (wait)")
        elif flagError:
            flagError = False
            errMessage = await client.send_message(config.main_group, 'SERVER STATUS OFFLINE🔴')
            logging.warning("check Coin scalper Bot (server status offline)")
        else:
            await client.delete_messages(config.source_group, res.id)
            res = await client.send_message(config.source_group, "!server status")
            logging.info("check Coin scalper Bot (wait)")
        await asyncio.sleep(config.timeout)

if __name__ == '__main__':
    client.start()
    logging.info("start Coin scalper checker Bot")
    client.loop.run_until_complete(main())
