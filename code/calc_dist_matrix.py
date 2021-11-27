### packages
import pandas as pd
from geopy.distance import geodesic
import numpy as np
import os

### working directory paths
#get the current working directory
current_directory = os.getcwd()
#go up a level in the directory path to get to the "final-project-dabp" folder
path_parent = os.path.dirname(current_directory)

### import data
df_cen = pd.read_csv(os.path.join(path_parent, "data", "02-processed", "census_geo.csv"))
df_pod = pd.read_csv(os.path.join(path_parent, "data", "02-processed", "pod_geo.csv"))

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
np.savetxt(os.path.join(path_parent, "data", "02-processed", "distance_matrix.csv"), distances, delimiter=",", fmt = '%5.2f')