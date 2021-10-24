### packages
import pandas as pd
from geopy.distance import geodesic
import numpy as np

### import data
df_cen = pd.read_csv('..\\data\\02-processed\\census_geo.csv')
df_pod = pd.read_csv('..\\data\\02-processed\\pod_geo.csv')

### store lat/longs in lists of tuples
cen_list = list(zip(df_cen['intptlat'], df_cen['intptlong']))
pod_list = list(zip(df_pod['lat'], df_pod['long']))

### calculate matrix of distances
dist_list = []
for i in range(len(cen_list)):
    row = []
    for j in range(len(pod_list)):
        d = geodesic(cen_list[i], pod_list[j]).miles
        row.append(d)
    dist_list.append(row)

distances = np.array(dist_list)
print(distances.shape)

### export
np.savetxt('..\\data\\02-processed\\distance_matrix.csv', distances, delimiter=",", fmt = '%5.2f')
