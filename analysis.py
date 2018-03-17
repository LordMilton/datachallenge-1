#imports
import pandas as pd
import datetime


racers = pd.read_csv('racers.csv')
races = pd.read_json('races.json')


racers['birth date'] = pd.to_datetime(racers['birth date'], format="%m/%d/%y")

temp = []
for date in racers['birth date']:
    if date >= datetime.datetime.strptime('2018-01-01', "%Y-%m-%d"):
        date = date - datetime.timedelta(days = 36525)
        temp.append(date)
        print(date)
    else:
        temp.append(date)
racers['birth date'] = temp
#birth = datetime.datetime.strptime(racers['birth date'], "%m/%d/%y")