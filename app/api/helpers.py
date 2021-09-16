from datetime import datetime, time

def days_to_birthday(birthday):
    now = datetime.now()
    today_earliest_time = datetime.combine(datetime.now(), time.min)
    
    if birthday is None:
        return
    # calculate by using the latest time of the day
    delta1 = datetime(now.year, birthday.month, birthday.day)
    delta2 = datetime(now.year+1, birthday.month, birthday.day)
    if delta1 >= today_earliest_time:
        return (delta1 - today_earliest_time).days
    else:
        return (delta2 - today_earliest_time).days
