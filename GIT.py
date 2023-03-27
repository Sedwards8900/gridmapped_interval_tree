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

'''
Grid-Mapped Interval Tree Class
'''
class GIT:
    sf_xmin = 0
    sf_xmax = 0
    sf_ymin = 0
    sf_ymax = 0
    delta_x = 0
    delta_y = 0

    def __init__(self):
        # Create empty grid
        self.git_grid = {}

    def __str__(self):
        return 'G-IT Index SF:({sf_xmin}, {sf_ymin}):({sf_xmax}, {sf_ymax}), deltaX:{delta_x}, deltaY:{delta_y}'.format(
            sf_xmin=self.sf_xmin,
            sf_ymin=self.sf_ymin,
            sf_xmax=self.sf_xmin,
            sf_ymax=self.sf_ymax,
            delta_x=self.delta_x,
            delta_y=self.delta_y)  # replace as needed

    def insert(self, trajectory):
        id = trajectory.get_id()
        pairs = trajectory.get_tgpairs()
        print(pairs)

        for index, row in pairs.iterrows():
            # Get tuple of (minx, miny, maxx, maxy)
            boundaries = row['geom'].bounds
            
            # Adjust size of grid according to trajectory boundaries
            if < self.sf_xmin:
                self.sf_min
            
            print(boundaries)


    def delete_by_id(self):
        pass

    def t_window(self):
        pass

    def sp_window(self):
        pass

    def st_window(self):
        pass


