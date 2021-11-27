### packages
import requests
import json
import pandas as pd
import numpy as np
import os

### working directory paths
#get the current working directory
current_directory = os.getcwd()
#go up a level in the directory path to get to the "final-project-dabp" folder
path_parent = os.path.dirname(current_directory)

### load and prep Census Gazetteer data (representative lat/long)
# https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.2019.html
df_geo = pd.read_csv('https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2019_Gazetteer/2019_gaz_tracts_42.txt', sep = '\t')
df_geo['GEOID'] = df_geo['GEOID'].astype(str)
df_geo.columns = df_geo.columns.str.lower().str.strip()

### load and prep ACS population, hh, and vehicle data
# define parameters for ACS API call
# variables: https://api.census.gov/data/2019/acs/acs5/variables.html
year = '2019' # 2019 ACS
est_yr = '5' # 5-year estimates
state = '42' # 42 = pennsylvania
county = '003' # 003 = allegheny county
geo = 'tract' # census tracts
variables = {'B01003_001E':'pop_tot',
             'B11016_001E':'num_hh_tot',
             'B25046_001E':'num_vehicles_tot'}

# build url
# API guidance: https://www.census.gov/programs-surveys/acs/guidance/handbooks/api.html
variables_keys = ','.join(variables.keys()) # create variable key string

url = (f'''https://api.census.gov/data/{year}/acs/acs{est_yr}?get={variables_keys}&for={geo}:*&in=state:{state}&in=county:{county}''')

# request and format data
headers = {'Content-Type': 'application/json'}
response = requests.get(url, headers = headers)
if response.status_code == 200:
    data = json.loads(response.content.decode('utf-8'))

# dataframe, rename
df = pd.DataFrame(data)
df = df.rename(columns = df.iloc[0]).drop([0])
df = df.rename(columns = variables)

# replace missings
df = df.replace('-666666666', np.NaN)

# rearrange columns
df_cols = df.columns.to_list()
df_cols = df_cols[-3:] + df_cols[:-3]
df = df[df_cols]

# to numeric
df[df.columns[3:]] = df[df.columns[3:]].apply(pd.to_numeric)

# calculate avg vehicles per hh, assign low vehicle access flag
df.loc[df['num_hh_tot'] > 0, 'avg_vehicle_per_hh'] = df['num_vehicles_tot'] / df['num_hh_tot']
def va_group(row):
    if row['avg_vehicle_per_hh'] <= df['avg_vehicle_per_hh'].quantile(0.25):
        val = 1
    else:
        val = 0
    return val
df['low_vehicle_access'] = df.apply(va_group, axis = 1)

### merge ACS with Census Gazetteer data
df['geoid'] = df['state'] + df['county'] + df['tract']
df = df.merge(df_geo, how = 'left', on = 'geoid')

# drop
df = df.drop(columns = ['usps', 'aland', 'awater', 'aland_sqmi', 'awater_sqmi'], axis = 1)

# checks
df.head()
df.shape
df.dtypes
sum(df['pop_tot'])
sum(df['num_hh_tot'])

# export
df.to_csv(os.path.join(path_parent, "data", "02-processed", "census_geo.csv"), index = False)