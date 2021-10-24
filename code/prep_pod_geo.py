### packages
import pandas as pd
import censusgeocode as cg

### read pod data
df = pd.read_excel('..\\data\\01-raw\\POD Sites.xlsx')
df = df[['SCHOOL/FACILITY NAME' ,'STRIP MAP']]
df = df.rename(columns = {'SCHOOL/FACILITY NAME':'pod', 'STRIP MAP':'pod_address'})
df['pod_address'] = df['pod_address'].str.replace('GOOGLE MAPS: ', '')
df = df.dropna(subset = ['pod_address'])

### geocode lat/long
lat = dict()
long = dict()
for i in range(len(df['pod_address'])):
    result = cg.onelineaddress(df['pod_address'][i], returntype='locations')
    if len(result) > 0:
        coords = result[0].get('coordinates')
        lat[i] = coords.get('y')
        long[i] = coords.get('x')

# map lat/longs to df
df['lat'] = df.index.to_series().map(lat)
df['long'] = df.index.to_series().map(long)

# manually fill remaining lat/long
df[df['long'].isnull() == True]
df['lat'].iloc[5] = 40.424549
df['long'].iloc[5] = -80.097329
df['lat'].iloc[9] = 40.507647
df['long'].iloc[9] = -80.163521
df['lat'].iloc[12] = 40.364780
df['long'].iloc[12] = -79.788885
df['lat'].iloc[21] = 40.513542
df['long'].iloc[21] = -80.217358
df['lat'].iloc[28] = 40.658484
df['long'].iloc[28] = -80.014887
df['lat'].iloc[37] = 40.300361
df['long'].iloc[37] = -79.991020

# view
df.head(10)

# export
df.to_csv('..\\data\\02-processed\\pod_geo.csv', index = False)
