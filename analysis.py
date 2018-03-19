import pandas as pd
import datetime

#%%
#cleaning
races = pd.read_json("races.json")
racers = pd.read_csv("racers.csv")

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

races = races[['event', 'start', 'finish', 'runner first', 'runner last']]
racers = racers[['first', 'mid', 'last', 'birth date']]

races['start'] = pd.to_datetime(races['start'], format='%H:%M:%S')
races['finish'] = pd.to_datetime(races['finish'], format='%H:%M:%S')
races['time'] = races['finish'] - races['start']
#removing anything faster than the fastest recorded marathon time 02:02:57
races = races[races.time >= datetime.timedelta(hours=2, minutes=2, seconds=57)]
del(races['finish'])
del(races['start'])
print(races)
#%%
#splitting
racers['first'] = racers['first'] +' '+ racers['mid'] + '.'
racers = racers[['first', 'last', 'birth date']]
old_racers = racers[racers['birth date'] < datetime.datetime.strptime('1988-01-01', "%Y-%m-%d")]
young_racers = racers[racers['birth date'] >= datetime.datetime.strptime('1988-01-01', "%Y-%m-%d")]
#%%
#merging
old_races = pd.merge(old_racers, races, left_on=['first', 'last'], right_on=['runner first', 'runner last'])
del(old_races['runner first'])
del(old_races['runner last'])
del(old_races['birth date'])
young_races = pd.merge(young_racers, races, left_on=['first', 'last'], right_on=['runner first', 'runner last'])
del(young_races['runner first'])
del(young_races['runner last'])
del(young_races['birth date'])

#%%
#analysis
del(old_races['last'])
del(old_races['first'])
del(young_races['last'])
del(young_races['first'])

#%%
old_races['age'] = ['old'] * len(old_races.time)
young_races['age'] = ['young'] * len(young_races.time)
allRaces_byAge = old_races.append(young_races)
#%%
allRaces_byAge.boxplot(column='time', by='age', notch=True)
print(allRaces_byAge.time.min()) 