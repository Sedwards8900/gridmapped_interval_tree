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
import random as rd

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


# Use insert function from GIT.py

# Insert ALL trajectories into GIT instance created -> This process will take a long time
# for traj in trajs:
#     git_traj.insert(traj)

# Insert 100 randomly selected trajectories
# rand_t = rd.choices(trajs, k=100)
# for traj in rand_t:
#     git_traj.insert(traj)

# Individually insert trajectories as below once uncommented for faster testing
git_traj.insert(trajs[0])
git_traj.insert(trajs[1])


# Use Delete function by eliminating trajectory within GIT based on provided ID
git_traj.delete_by_id(trajs[0].get_id())
git_traj.delete_by_id(trajs[0].get_id())


# Test temporal window query function by giving to time points

# Create time points where t1 < t2 as they must be ordered for method to work
# t = tdf.sample(n=2)['ts']
# t1 = t.iloc[0]
# t2 = t.iloc[-1]

# Specifically chosen for testing purposes
t1 = tdf.iloc[0]['ts']
t2 = tdf.iloc[1]['ts']


if t2 > t1:
    print(git_traj.t_window((t1, t2)))
else:
    print(git_traj.t_window((t2, t1)))
