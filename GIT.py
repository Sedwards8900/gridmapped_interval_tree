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

from shapely.geometry import Polygon
from intervaltree import IntervalTree
from collections import defaultdict
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
                    # Add 9 mins 59 seconds to interval to indicate it reaches until before next segment begins
                    end = end + timedelta(seconds=599) # No overlap on segments per say

                    # Convert to simple datetime format for interval manipulation
                    start = start.to_pydatetime()
                    end = end.to_pydatetime()

                    # Store interval into intervaltree instance within specified grid cell
                    if not self.git_grid[key].containsi(start, end, traj_id):
                        self.git_grid[key][start:end] = traj_id
                    else:
                        print(f"Trajectory with id # {traj_id} already exists within GIT")
                        return
                    
                    # Reset flags to start over or end loop
                    done = False
                    started = False
        print(f"Inserted trajectory with id # {traj_id} into GIT")
        
        # # Grid content confirmation
        # for key in self.git_grid:
        #     if not self.git_grid[key].is_empty():
        #         print(key, " : ", self.git_grid[key])




    '''
    Method that deletes all related tgpairs within the grid-mapped interval tree based on 
    trajectory ID provided.
    '''
    def delete_by_id(self, traj_id):
        deleted = []
        found = False
        # Review each grid for values within dictionary
        for key in self.git_grid:
            # If grid cell tree is not empty, proceed to check for interval vals
            if not self.git_grid[key].is_empty():
                
                # Loop through intervals within tree
                for interval in self.git_grid[key]:
                    # If data containing trajectory id equals to given id, remove from tree
                    if interval.data == traj_id:
                        deleted.append((interval))
                        found = True

                # Remove found intervals from tree in specific grid
                for elem in deleted:
                    self.git_grid[key].remove(elem)
                # Reset intervals to be deleted
                deleted = []

        if found:
            print(f"Deleted trajectory with id # {traj_id} from GIT")
        else:
            print(f"Trajectory with id # {traj_id} not found GIT")
        
        # # Grid content confirmation
        # for key in self.git_grid:
        #     if not self.git_grid[key].is_empty():
        #         print(key, " : ", self.git_grid[key])


    '''
    Temporal window query: Given two (ordered) time points (t1, t2) which represent a 
    time range, find all trajectory identifiers that temporally overlap with the 
    given temporal range.
    '''
    def t_window(self, time_tuple):
        # Set interval values to same type within interval tree object
        start = time_tuple[0].to_pydatetime()
        end = time_tuple[1].to_pydatetime()

        # Set variable to store all ids for trajectories
        overlaps = set()
        
        # Access each tree per grid cell
        for key in self.git_grid:

            if not self.git_grid[key].is_empty():
                # Check if overlap in time occurs, returns a set variable
                temp = self.git_grid[key][start:end]
                # Extract traj ids from set
                if temp:
                    for interval in temp:
                        # ranges are inclusive of the lower limit, but non-inclusive of the upper limit
                        overlaps.add(interval.data) 
        if overlaps:
            return overlaps
        else:
            return(f"No trajectory found overlaping given time range")

    
    '''
    Spatial window query: Given two coordinates (i.e., (x1, y1), (x2, y2)) that will 
    represent a bounding box (envelope), find all trajectory identifiers that spatially 
    overlap with the given box.
    '''
    def sp_window(self, c1, c2):
        overlaps = set()
        # Access each tree per grid cell
        for key in self.git_grid:
            if not self.git_grid[key].is_empty():

                # If grid cell and box as Polygons intersect, obtain data from each interval within
                box = Polygon([(c1[0], c1[1]),(c1[0],c2[1]),(c2[0],c2[1]),(c2[0],c1[1])])
                cell = Polygon([(key[0],key[1]),(key[0],key[3]),(key[2],key[1]),(key[2],key[3])])
                if box.intersects(cell):
                    for interval in self.git_grid[key]:
                        overlaps.add(interval.data)
        if overlaps:
            return overlaps
        else:
            return(f"No trajectory found overlaping given spatial bounding box")


    '''
    Spatio-temporal window query: Given an envelope (defined using two coordinates, as 
    in the spatial window query) and a time range (defined using two time points, 
    as in the temporal query), find all trajectory identifiers that both spatially 
    and temporally overlap with the given envelope and time range.
    '''
    def st_window(self, c1, c2, time_tuple):
        overlaps = set()
        # Set interval values to same type within interval tree object
        start = time_tuple[0].to_pydatetime()
        end = time_tuple[1].to_pydatetime()

        # Access each tree per grid cell
        for key in self.git_grid:
            if not self.git_grid[key].is_empty():

                # If grid cell and box as Polygons intersect, proceed to check for intervals
                box = Polygon([(c1[0], c1[1]),(c1[0],c2[1]),(c2[0],c2[1]),(c2[0],c1[1])])
                cell = Polygon([(key[0],key[1]),(key[0],key[3]),(key[2],key[1]),(key[2],key[3])])
                
                if box.intersects(cell):
                    # Check if overlap in time occurs, returns a set variable
                    temp = self.git_grid[key][start:end]
                    if temp:
                        for interval in temp:
                            # ranges are inclusive of the lower limit, but non-inclusive of the upper limit
                            overlaps.add(interval.data)

        if overlaps:
            return overlaps
        else:
            return(f"No trajectory found overlaping given spatio-temporal bounding box")


