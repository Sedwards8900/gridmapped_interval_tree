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

# ++++++++++++++++++++++++
# REQUIREMENT 1 COMPLETION:

# Converting data into trajectories by first extracting traj.ids
traj_ids = tdf.id.unique()

# Creating list containing all trajectories
trajs = []
for elem in traj_ids:
    tgpairs = tdf.loc[tdf['id'] == elem, ['ts', 'geom']]
    tgpairs = tgpairs.set_index(['ts'])
    trajs.append(Trajectory(elem, tgpairs))


# ++++++++++++++++++++++++
# REQUIREMENT 2 COMPLETION:

# Find desired grid size by getting tuple of (minx, miny, maxx, maxy)
b = tdf['geom'].bounds
delta_x = 200 # Only use multiples of 2 for size of grid
delta_y = 200 # Only use multiples of 2 for size of grid
boundaries = [b['minx'].min(), b['miny'].min(), b['maxx'].max(), b['maxy'].max()]
range_x = int(math.ceil((boundaries[2]-boundaries[0])/200.0)*200)
range_y = int(math.ceil((boundaries[3]-boundaries[1])/200.0)*200)
boundaries = [-range_x//2, -range_y//2, range_x//2, range_y//2]
print(boundaries)

# Create instance GIT (Grid-Mapped Interval Tree) with info above
git_traj = GIT(boundaries, delta_x, delta_y)
print(git_traj)

# =================INSERT FUNCTION=================

# You may use any of the three forms of selecting and inserting below
# Depending on the amount of trajectories you wish to add

# Insert 50 randomly selected trajectories
rand_t = rd.sample(trajs, 50)
for traj in rand_t:
    git_traj.insert(traj)

# Insert ALL trajectories into GIT instance created -> This process will take a long time
# for traj in trajs:
#     git_traj.insert(traj)

# Individually insert trajectories as below once uncommented for faster testing
# git_traj.insert(trajs[0])
# git_traj.insert(trajs[1])


# =================DELETE FUNCTION=================

# Use Delete function by eliminating trajectory within GIT based on provided ID
git_traj.delete_by_id(trajs[1].get_id())
git_traj.delete_by_id(trajs[1].get_id())


# =================T_WINDOW FUNCTION=================

# Test temporal window query function by giving to time points

# Specifically chosen for testing purposes
t1 = tdf.iloc[0]['ts']
t2 = tdf.iloc[1]['ts']

# Create time points where t1 < t2 as they must be ordered for method to work
# t = tdf.sample(n=2)['ts']
# t1 = t.iloc[0]
# t2 = t.iloc[-1]

if t2 > t1:
    print(git_traj.t_window((t1, t2)))
else:
    print(git_traj.t_window((t2, t1)))


# =================SP_WINDOW FUNCTION=================

# Test spatial window query function that returns trajectory ids if
# given box from two tuples overlaps with a grid containing intervals
c1 = (-300, -400) # Input values between -1100 and 1100
c2 = (100, 200) # Input values between -800 and 800
print(git_traj.sp_window(c1, c2))
