'''
Insert toy dataset into a G-IT index instance, then create two test cases
for each query and show your results

'''
import os
from Util import tdf
from Trajectory import Trajectory
from GIT import GIT
import pandas as pd
import math

# Converting data into trajectories

# Extracting traj.ids
traj_ids = tdf.id.unique()


# REQUIREMENT 1 COMPLETION:

# Creating list containing all trajectories
trajs = []
for elem in traj_ids:
    tgpairs = tdf.loc[tdf['id'] == elem, ['ts', 'geom']]
    tgpairs = tgpairs.set_index(['ts'])
    trajs.append(Trajectory(elem, tgpairs))
    # if elem == 2415: # Checking format of df has ts as index
    #     print(tgpairs)


# REQUIREMENT 2 COMPLETION:

# Find desired grid size by getting tuple of (minx, miny, maxx, maxy)
b = tdf['geom'].bounds
delta_x = 200 
delta_y = 200
boundaries = [b['minx'].min(), b['miny'].min(), b['maxx'].max(), b['maxy'].max()]
range_x = int(math.ceil((boundaries[2]-boundaries[0])/200.0)*200)
range_y = int(math.ceil((boundaries[3]-boundaries[1])/200.0)*200)
boundaries = [-range_x//2, -range_y//2, range_x//2, range_y//2]
# print(boundaries)

# Create instance GIT (Grid-Mapped Interval Tree) with info above
git_traj = GIT(boundaries, delta_x, delta_y)
print(git_traj)

# Insert trajectories into GIT instance created
# for traj in trajs:
#     git_traj.insert(traj)

# Test solo trajectory for development purposes
git_traj.insert(trajs[0])