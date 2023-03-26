'''
Insert toy dataset into a G-IT index instance, then create two test cases
for each query and show your results

'''
import os
from Util import tdf
from Trajectory import Trajectory
from GIT import GIT

# Testing if data passed through
# print(tdf.head(1))
# print(tdf['ts'])
# print(tdf.head(1)['geom'])

# Converting data into trajectories

# Extracting traj.ids
traj_ids = tdf.id.unique()
print(traj_ids)

# Creating list containing all trajectories
trajs = []
for elem in traj_ids:
    tgpairs = tdf.loc[tdf['id'] == elem, ['ts', 'geom']]
    # tgpairs = list(zip(tgpairs['ts'], tgpairs['geom'])) # tuple way
    trajs.append(Trajectory(elem, tgpairs))

# Checking if list truly contains trajectories after execution of for loop
print(isinstance(trajs[0], Trajectory))
print(trajs[0])

# Create instance GIT (Grid-Mapped Interval Tree) and insert trajectories into it

'''
What I did was in TestGIT.py, I read the file using the function 
from Util.py. Convert them into trajectory objects. Create an 
instance of the GIT class from GIT.py. Insert all the trajectories 
into GIT. Then the rest of TestGIT.py is demonstrating that the 
query functions that are part of GIT.py.  

'''

git_traj = GIT(trajs[0]) # Define how this is gonna be started
