import datetime, calendar
def getweek():
    day = str(datetime.date.today())
    dt = datetime.datetime.strptime(day, '%Y-%m-%d')
    days = []
    for i in range(5):
        days.append(datetime.datetime.strftime(dt - datetime.timedelta(days=dt.weekday()-i), "%B %d"))
    return days