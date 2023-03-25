from telethon import TelegramClient, events, sync, Button
import re
from func import getweek, saveday
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
    workday = {}
    day = getweek()
    kbdays = [[Button.inline(day[0], b"d1")],[Button.inline(day[1], b"d2")],[Button.inline(day[2], b"d3")],[Button.inline(day[3], b"d4")],[Button.inline(day[4], b"d5")]]
    await bot.send_message(send_event.query.user_id, 'Выбери день', buttons=kbdays)
    @bot.on(events.CallbackQuery(data=re.compile(b'd1|d2|d3|d4|d5')))
    async def send_commandday_handler(send_event):
        await send_event.answer()
        match send_event.data:
            case b"d1":
                workday["day"] = day[0]
            case b"d2":
                workday["day"] = day[1]
            case b"d3":
                workday["day"] = day[2]
            case b"d4":
                workday["day"] = day[3]
            case b"d5":
                workday["day"] = day[4]
        kbworkh = [Button.inline("Полный день", b"wf"), Button.inline("Укажу промежуток", b"wnf")]
        await bot.send_message(send_event.query.user_id, 'Какая длина рабочего дня?', buttons=kbworkh)

        @bot.on(events.CallbackQuery(data=re.compile(b'wf|wnf')))
        async def send_command_workh_f(send_workh):
            if send_workh.data == b'wf':
                workday["startday"] = "10:00"
                workday["endday"] = "18:30"
                workday["place"] = "HQ"
                await send_workh.answer()
                await bot.send_message(send_workh.query.user_id, 'День записан!')
                await saveday(workday)
                # Нужно добавить проверку уже существующей записи в файле и предложить изменение или удаление
                print(workday)
            else:

                # Можно сделать красивый ввод в виде кнопок
                # Пока что реализую в виде отправки сообщения в формате ЧЧ:ММ
                #kbshours = [[Button.inline("10:00", b"10:00"), Button.inline("10:30", b"10:30"), Button.inline("11:00", b"11:00"), Button.inline("11:30", b"11:30"), Button.inline("12:00", b"12:00")]
                           # [Button.inline("12:30", b"12:30"), Button.inline("13:00", b"13:00"), Button.inline("13:30", b"13:30"), Button.inline("14:00", b"14:00"), Button.inline("14:30", b"14:30")]]
                #await bot.send_message(send_workh.query.user_id, 'Выбери начало рабочего дня', buttons=kbshours)
                await bot.send_message("Введи час начала рабочего дня в формате ЧЧ:ММ")
                @bot.on(events.NewMessage(incoming=True, pattern=re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")))
                async def getworkstart(workst):
                    workday["startday"] = str(workst.data)
                    await bot.send_message("Введи час конца рабочего дня в формате ЧЧ:ММ")
                    @bot.on(events.NewMessage(incoming=True, pattern=re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")))
                    async def getworkend(workend):
                        workday["endday"] = str(workend.data)
                        workday["place"] = "HQ"
                        await bot.send_message(send_workh.query.user_id, 'День записан!')
                        await saveday(workday)
                        # То же, что в комменте в line 46
                        print(workday)
try:
    bot.run_until_disconnected()
finally:
    bot.disconnect()