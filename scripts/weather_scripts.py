import pandas as pd
import numpy as np
states = ['QLD1', 'NSW1', 'SA1', 'VIC1']
city_to_region = {'Adelaide': 'SA1', 'Melbourne': 'VIC1', 'Sydney': 'NSW1', 'Brisbane': 'QLD1'}

for state in states:
    df = pd.read_csv("files/historical_weather.csv", parse_dates=['dt_iso'], )
    df = df[['dt', 'city_name', 'temp', 'humidity', 'wind_speed', 'wind_deg', 'clouds_all']]
    df['city_name'] = df['city_name'].apply(lambda x: city_to_region[x])
    df = df.loc[df['city_name'] == state]
    df['humidity'] = df['humidity'].apply(lambda x: x/100) # Normalise humdity to between 0 (0% humdity) and 1 (100% humdity)
    df['clouds_all'] = df['clouds_all'].apply(lambda x: x/100)# Normalise cloud cover to between 0 (0% cloud) and 1 (100% cloud)
    df.columns = ['UNIXTIME', 'REGIONID', 'TEMP', 'HUMIDITY', 'SPEED', 'DIRECTION', 'CLOUD']

    df['DATETIME'] = pd.to_datetime(df['UNIXTIME'], unit='s')
    df['DATETIME'] = df['DATETIME'].dt.tz_localize('UTC').dt.tz_convert('Australia/Brisbane') # In the NEM we hate daylight savings
    df = df.drop_duplicates(subset=['DATETIME'])
    df.index = df['DATETIME']
    df = df.resample('30min').pad() # Magically make 60 minute weather data into 30 minutes weather data
    df = df[df['DATETIME'].dt.year > 2015]
    # Ignore this, it's probably fine
    df['DATETIME'] = df.index
    df['UNIXTIME'] = df.index.astype(np.int64) // 10 ** 9
    df = df.reset_index(level=0, drop=True).reset_index()
    del df['index']

    df.to_csv('{}-weather.csv'.format(state))