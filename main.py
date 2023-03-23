from telethon import TelegramClient, events, sync, Button
import re
from func import getweek
file = open('creds', 'r')
credentials = file.read().split('\n')
file.close()
bot = TelegramClient("1",credentials[0], credentials[1]).start(bot_token=credentials[2])

startkeyboardintern = [[Button.inline("Добавить день", b"1"), Button.inline("Посмотреть неделю", b"2")], [Button.inline("Всё расписание", b"3"), Button.inline("Экспорт в .xlsx", b"4")]]
startkeyboardadmin = [[Button.inline("Изменить день", b"1"), Button.inline("Всё расписание", b"2")], [Button.inline("Экспорт в .xlsx", b"4")]]
@bot.on(events.NewMessage(incoming=True, pattern='/start'))
async def handler(event):
    await bot.send_message(event.message.peer_id.user_id, '**Привет**, Чювак!\nВыбери действие:', buttons=startkeyboardintern)

@bot.on(events.CallbackQuery(data=b'1'))
async def send_command_handler(send_event):
    payload = {}
    await send_event.answer()
    day = getweek()
    kbdays = [[Button.inline(day[0], bytes(day[0], 'utf8'))],[Button.inline(day[1], bytes(day[1], 'utf8'))],[Button.inline(day[2], bytes(day[2], 'utf8'))],[Button.inline(day[3], bytes(day[3], 'utf8'))],[Button.inline(day[4], bytes(day[4], 'utf8'))]]
    await bot.send_message(send_event.query.user_id, 'Выбери день', buttons=kbdays)
    @bot.on(events.CallbackQuery(data2=bytes(re.match(r""+re.escape(day[0])+r"|"+re.escape(day[1])+r"|"+re.escape(day[2])+r"|"+re.escape(day[3])+r"|"+re.escape(day[4])+r"|"), 'utf8')))
    async def send_commandday_handler(send_event):
        await send_event.answer()
        await bot.send_message(send_event.query.user_id, 'Выбери жизн')

try:
    bot.run_until_disconnected()
finally:
    bot.disconnect()