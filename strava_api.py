#%%
import requests
import urllib3
#Using logigns instead of print
import logging
#Datetime will allow Python to recognize dates as dates, not strings.
from datetime import datetime

#Pandas will be the backbone of our data manipulation.
import pandas as pd
from pandas.io.json import json_normalize
#Seaborn is a data visualization library.
import seaborn as sns
#Matplotlib is a data visualization library. 
#Seaborn is actually built on top of Matplotlib. 
import matplotlib.pyplot as plt
#Numpy will help us handle some work with arrays.
import numpy as np


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.NOTSET)

logging.getLogger('matplotlib.font_manager').disabled = True

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "64115",
    'client_secret': 'a9f44c6b3206f26b80b5b435b542203972de4472',
    'refresh_token': 'c101042fde9c155647353200eae76387d8c47f52',
    'grant_type': "refresh_token",
    'f': 'json'
}

logging.info("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
logging.info("Access Token Successful".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

logging.info('Everything is normal. Relax!')

print(my_dataset[0]["name"])
print(my_dataset[0]["map"]["summary_polyline"])

activities = json_normalize(my_dataset)

# Create new dataframe with only columns I care about
cols = ['name', 'upload_id', 'type', 'distance', 'moving_time',   
         'average_speed', 'max_speed','total_elevation_gain',
         'start_date_local'
       ]

logging.info(cols)

activities = activities[cols]

#Break date into start time and date
activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date_local'] = activities['start_date_local'].dt.date

logging.info(activities.head(5))

logging.info(activities['type'].value_counts())

runs = activities.loc[activities['type'] == 'Run']

logging.info(runs.head(5))

sns.set(style="ticks", context="talk")
sns.scatterplot(x='distance', y = 'average_speed', data = runs).set_title("Average Speed vs Distance")

sns.scatterplot(x='distance', y = 'max_speed', data = runs).set_title("Max Speed vs Distance")

plt.savefig('save_as_a_png.png')


# max speed over time
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.asarray(runs.start_date_local)
y = np.asarray(runs.max_speed)
ax.plot_date(x, y)
ax.set_title('Max Speed over Time')
fig.autofmt_xdate(rotation=45)
fig.tight_layout()
plt.savefig('save_as_a_png2.png')

fig = plt.figure()
ax1 = fig.add_subplot(111)
x = np.asarray(runs.start_date_local)
y = np.asarray(runs.average_speed)
ax1.plot_date(x, y)
ax1.set_title('Average Speed over Time')
fig.autofmt_xdate(rotation=45)
fig.tight_layout()
fig.show()

plt.savefig('save_as_a_png3.png')