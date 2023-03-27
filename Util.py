import pandas as pd
import geopandas
from shapely import wkt

'''
Reader function that decompresses a csv file containing trajectory data for toy object needed in 
homework 2 assignment for Spatial Databases.
Parameters:
    path = path to csv compressed file
    column_names = names of columns for dataframe once created, format is a list with 3 strings

Returns:
    a dataframe

'''
def read_toy_dataset(path, column_names):
    # Read and save as dataframe after decompressing csv file, no header available, 
    # adding a tab as a separator between each val found and using the column names given
    traj_df = pd.read_csv(filepath_or_buffer=path, compression='gzip', header=None, sep='\t', names=column_names)
    
    # Column ts converted to datetime format, i.e. 1353775800000 => 2012-11-24 16:50:00
    traj_df['ts'] = pd.to_datetime(traj_df['ts'], unit='ms')

    # Convert into a geometry
    traj_df['geom'] = traj_df['geom'].apply(wkt.loads)
    traj_df = geopandas.GeoDataFrame(traj_df, geometry='geom')

    # Return geodataframe
    return traj_df

# Set up file path and column values, then call the function to create geo-df
path = './toy_traj.csv.gz'
columns = ['id', 'ts', 'geom']
tdf = read_toy_dataset(path, columns)
# print(tdf.info())