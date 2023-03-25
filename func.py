import datetime, calendar, pickle, os
def getweek():
    day = str(datetime.date.today())
    dt = datetime.datetime.strptime(day, '%Y-%m-%d')
    days = []
    for i in range(5):
        days.append(datetime.datetime.strftime(dt - datetime.timedelta(days=dt.weekday()-i), "%B %d"))
    return days
def saveday(dict):
    if os.path.isfile("shifts.pickle"):
        with open('shifts.pickle', 'ab') as handle:
            pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open('shifts.pickle', 'wb') as handle:
            pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)