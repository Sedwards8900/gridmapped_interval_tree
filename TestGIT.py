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

# REQUIREMENT 1 COMPLETION:

# Creating list containing all trajectories
trajs = []
for elem in traj_ids:
    tgpairs = tdf.loc[tdf['id'] == elem, ['ts', 'geom']]
    # tgpairs = list(zip(tgpairs['ts'], tgpairs['geom'])) # tuple way
    trajs.append(Trajectory(elem, tgpairs))

# Checking if list truly contains trajectories after execution of for loop
# print(isinstance(trajs[0], Trajectory))
# print(trajs[0])

# REQUIREMENT 2 COMPLETION:
# Create instance GIT (Grid-Mapped Interval Tree) and insert trajectories into it
git_traj = GIT()
print(git_traj)

# Insert all trajectories into GIT instance created
# for traj in trajs:
#     git_traj.insert(traj)

git_traj.insert(trajs[0])

'''
What I did was in TestGIT.py, I read the file using the function 
from Util.py. Convert them into trajectory objects. Create an 
instance of the GIT class from GIT.py. Insert all the trajectories 
into GIT. Then the rest of TestGIT.py is demonstrating that the 
query functions that are part of GIT.py.  

'''

'''
Yeah. trajectory.py is the class definition for trajectories. 
He didn't really specify so this is the way I interpreted it. 
I figured that since you had a insert function. That means you 
want to actually insert the trajectories into the index class 
one by one. So I interpreted it as TestGIT.py calls the function 
in Util.py to read the dataset. You convert them into trajectories. 
Then create an instance of GIT and insert the trajectories into it.

You could also just read the dataset, pass it all into GIT as 
part of the constructor where it converts it into trajectories.
'''

'''
Yeah. So the simplest is just reading in the data, looping over it 
looking for the min and the max. I skipped that step and just represented 
the grid as a dictionary. You have to fix a grid size regardless so what 
I did was just compute the grid coordinates use the grid coordinates 
as my key for the dictonary and check to see if the key exists if it 
doesn't i create a new entry with that key and create a interval tree 
as the value of the dictionary if it does, i just insert the time tuple 
into the tree.

For the sake of his requirement. It seemed like he wanted to know the 
size of the space. Every time an entry is loaded, I compare it to the 
min & max and replace if its is outside that box

'''