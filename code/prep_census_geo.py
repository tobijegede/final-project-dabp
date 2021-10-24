### packages
import requests
import json
import pandas as pd

### load and prep Census Gazetteer data (representative lat/long)
# https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.2019.html
df_geo = pd.read_csv('https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2019_Gazetteer/2019_gaz_tracts_42.txt', sep = '\t')
df_geo['GEOID'] = df_geo['GEOID'].astype(str)
df_geo.columns = df_geo.columns.str.lower()

### load and prep ACS population and hh data
# define parameters for ACS API call
# variables: https://api.census.gov/data/2019/acs/acs5/variables.html
year = '2019' # 2019 ACS
est_yr = '5' # 5-year estimates
state = '42' # 42 = pennsylvania
county = '003' # 003 = allegheny county
geo = 'tract' # census tracts
variables = {'B01003_001E':'pop_tot',
             'B11016_001E':'num_hh_tot',
             'B11016_002E':'num_fam_hh_tot',
             'B11016_003E':'num_fam_hh_2p',
             'B11016_004E':'num_fam_hh_3p',
             'B11016_005E':'num_fam_hh_4p',
             'B11016_006E':'num_fam_hh_5p',
             'B11016_007E':'num_fam_hh_6p',
             'B11016_008E':'num_fam_hh_7plus',
             'B11016_009E':'num_nonfam_hh_tot',
             'B11016_010E':'num_nonfam_hh_1p',
             'B11016_011E':'num_nonfam_hh_2p',
             'B11016_012E':'num_nonfam_hh_3p',
             'B11016_013E':'num_nonfam_hh_4p',
             'B11016_014E':'num_nonfam_hh_5p',
             'B11016_015E':'num_nonfam_hh_6p',
             'B11016_016E':'num_nonfam_hh_7plus'}

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

# rearrange columns
df_cols = df.columns.to_list()
df_cols = df_cols[-3:] + df_cols[:-3]
df = df[df_cols]

# to numeric
df[df.columns[3:]] = df[df.columns[3:]].apply(pd.to_numeric)

# combine family + nonfamily counts
df['num_hh_1p'] = df['num_nonfam_hh_1p']
df['num_hh_2p'] = df['num_fam_hh_2p'] + df['num_nonfam_hh_2p']
df['num_hh_3p'] = df['num_fam_hh_3p'] + df['num_nonfam_hh_3p']
df['num_hh_4p'] = df['num_fam_hh_4p'] + df['num_nonfam_hh_4p']
df['num_hh_5p'] = df['num_fam_hh_5p'] + df['num_nonfam_hh_5p']
df['num_hh_6p'] = df['num_fam_hh_6p'] + df['num_nonfam_hh_6p']
df['num_hh_7plus'] = df['num_fam_hh_7plus'] + df['num_nonfam_hh_7plus']
df = df.loc[:, ~df.columns.str.startswith('num_fam_hh_')]
df = df.loc[:, ~df.columns.str.startswith('num_nonfam_hh_')]

### merge ACS with Census Gazetteer data
df['geoid'] = df['state'] + df['county'] + df['tract']
df = df.merge(df_geo, how = 'left', on = 'geoid')

# checks
df.head()
df.shape
sum(df['pop_tot'])

# export
df.to_csv('..\\data\\02-processed\\census_geo.csv', index = False)
