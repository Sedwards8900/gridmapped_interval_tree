'''
To create the G-IT index structure, you will use a fixed spatial grid, defined using six parameters:

● sf_xmin: minimum x-coordinate value for the spatial framework
● sf_xmax: maximum x-coordinate value for the spatial framework
● sf_ymin: minimum y-coordinate value for the spatial framework
● sf_ymax: maximum y-coordinate value for the spatial framework
● Δx: step size for grid cells in x-dimension
● Δy: step size for grid cells in y-dimension

Based on these parameters, you will have an nx by ny spatial grid where,
nx = ⌈(sf_xmax-sf_xmin) / Δx⌉ ny = ⌈(sf_ymax-sf_ymin) / Δy⌉

This means, there is no temporal overlap allowed between time extent of the discretely 
represented time-geometry pairs and temporal objects have a total order.
Grid-mapped interval trees (G-IT) index is a simple trajectory access mechanism 
primarily designated for historical persistent spatiotemporal data. The index is 
built mainly upon a spatial grid to partition the spatial dimension and each grid 
cell has a pointer to an R-tree based interval tree index. Interval trees often refer 
to degenerate R-trees, which means instead of indexing 2-dimensional space, they are 
used for indexing 1 dimension (which is often time intervals).

'''

from Trajectory import Trajectory
from shapely.geometry import Polygon
from intervaltree import Interval, IntervalTree
from collections import defaultdict
import pandas as pd
from datetime import timedelta

'''
Grid-Mapped Interval Tree Class
'''
class GIT:
    # Instances of class GIT
    sf_xmin = 0
    sf_xmax = 0
    sf_ymin = 0
    sf_ymax = 0
    delta_x = 0
    delta_y = 0
    git_grid = defaultdict(list)

    def __init__(self, x_y_min_max_list, delta_x, delta_y):
        # Set instances of class to be equal to given values
        self.sf_xmin = x_y_min_max_list[0]
        self.sf_xmax = x_y_min_max_list[2]
        self.sf_ymin = x_y_min_max_list[1]
        self.sf_ymax = x_y_min_max_list[3]
        self.delta_x = delta_x
        self.delta_y = delta_y

        # Create grid as dictionary where each grid cell is an interval tree
        # Each key of the dictionary is formatted as: (minx miny maxx maxy)
        tempminx = self.sf_xmin
        tempminy = self.sf_ymin
        while tempminx != self.sf_xmax:
            while tempminy != self.sf_ymax:
                self.git_grid[(tempminx, tempminy, tempminx + self.delta_x, tempminy + self.delta_y)] = IntervalTree()
                tempminy += self.delta_y
            tempminx += self.delta_x
            tempminy = self.sf_ymin
        # print(list(self.git_grid.keys())) #Checking to see grid format

    def __str__(self):
        return 'G-IT Index SF:({sf_xmin}, {sf_ymin}):({sf_xmax}, {sf_ymax}), deltaX:{delta_x}, deltaY:{delta_y}'.format(
            sf_xmin=self.sf_xmin,
            sf_ymin=self.sf_ymin,
            sf_xmax=self.sf_xmin,
            sf_ymax=self.sf_ymax,
            delta_x=self.delta_x,
            delta_y=self.delta_y)  # replace as needed

    def insert(self, trajectory):
        # Extract values from trajectory given including id and tspairs
        traj_id = trajectory.get_id()
        tgpairs = trajectory.get_tgpairs()
        tgpairs = tgpairs.sort_index()
        
        # Find out if segment belongs to a grid block
        for key in self.git_grid: # (minx miny maxx maxy)
            # Set start and end times to 0
            intv = []
            start = 0
            end = 0
            # Set boolean flags to handle when to start and insert interval
            started = False
            done = False

            # Navigate through tgpairs to check on geometry intersection
            for ts, row in tgpairs.iterrows():
                
                # If grid cell as Polygon and geom intersect, set start and end times
                cell = Polygon([(key[0],key[1]),(key[0],key[3]),(key[2],key[1]),(key[2],key[3])])
                if row['geom'].intersects(cell):

                    # Set flag to True to indicate beginning of segment within grid cell and
                    # initiate start value of interval
                    if not started:
                        started = True
                        start = ts

                    # Set end value to current tgpair ts value
                    end = ts

                # If the geometry in row no longer within grid cell, set flag to false to trigger interval insert
                else:
                    if started:
                        done = True
                    
                # If segment done or this is the last row in the df while on a segment, add interval
                if done or (ts == tgpairs.index[-1] and started):
                    # Add 10 mins to interval to indicate it reaches until next segment begins
                    end = end + timedelta(minutes=10)

                    # Convert to simple datetime format for interval manipulation
                    start = start.to_pydatetime()
                    end = end.to_pydatetime()

                    # Store interval into intervaltree instance within specified grid cell
                    self.git_grid[key][start:end] = traj_id

                    # Reset flags to start over or end loop
                    done = False
                    started = False
        
        # Checking initial grid format after an insertion for testing purposes
        for key in self.git_grid:
            print(self.git_grid[key].is_empty())
            print(key, " : ", self.git_grid[key])

            if not self.git_grid[key].is_empty():
                print("\n\n")
                for interval in self.git_grid[key]:
                    print(interval)

    '''
    Method that deletes all related tgpairs within the grid-mapped interval tree based on 
    trajectory ID provided.
    '''
    def delete_by_id(self, traj_id):
        # # Review each grid for values within dictionary
        # for key in self.git_grid:
        #     # If grid cell tree is not empty, proceed to check for interval vals
        #     if not self.git_grid[key].is_empty():
        #         # If data containing trajectory id equals to given id, remove from tree
        #         if self.git_grid[key].data == traj_id:
        pass


    def t_window(self):
        pass

    def sp_window(self):
        pass

    def st_window(self):
        pass


