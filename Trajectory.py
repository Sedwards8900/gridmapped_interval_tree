'''
Implementation for Trajectory Data type

'''

class Trajectory:

  '''
  Defining class Trajectory elements

  '''
  def __init__(self, traj_id, tgpairs):
    # Id assigned to each trajectory
    self.traj_id = traj_id
    # time-geometry pairs that form a trajectory, in the form of a list
    self.tgpairs = tgpairs

  '''
  Function to print contents of trajectory object
  '''
  def __str__(self):
    return f"{self.traj_id} = [{self.tgpairs}]" # replace as needed => need to print time-geometry pairs



# t1 = Trajectory("John", None)
# print(t1)