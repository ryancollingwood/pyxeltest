import numpy as np
import math
from scipy.spatial import KDTree


class Grid():
    
    def __init__(self, x_max, y_max, tile_size):
        """
        Initiaise a grid
        :param x_max:
        :param y_max:
        :param tile_size:
        """
        
        # generate the indicies for our grid size
        # the indicies are the positions of our grid
        y_mesh, x_mesh = np.indices((y_max, x_max))
        
        # we want to store the center value in pixels for
        # our tiles
        self.tile_size = tile_size
        self.half_tile_size = (self.tile_size / 2.0)
        
        x_mesh = (x_mesh + 1) * self.half_tile_size
        y_mesh = (y_mesh + 1) * self.half_tile_size
        
        # let's persist center positions
        pixel_center_positions = np.squeeze(np.dstack([y_mesh.ravel(), x_mesh.ravel()]))
        # property `map_pixel_center_positions` is for assisting human lookups of the grid
        self.map_pixel_center_positions = np.squeeze(np.reshape(pixel_center_positions, (y_max, x_max, 2)))
        
        # property `flat_pixel_positions` is for assisting computer lookup of the grid and
        # reverse lookups for pixels to positions
        flat_pixel_positions = pixel_center_positions.flatten()
        self.flat_pixel_positions = np.reshape(flat_pixel_positions, (int(len(flat_pixel_positions) / 2), -1))
        
        # to find a position based on pixel position we'll use the scipy.spatial.KDTree data type
        self.tree = KDTree(self.flat_pixel_positions)
        
        # let's keep the last row, column values to minimise repeated lookups
        self.last_row = None
        self.last_column = None
        
        #
    
    def get_pixel_center(self, row, column):
        """
        Get the pixel enter of a given grid position
        :param row:
        :param column:
        :return:
        """
        return self.map_pixel_center_positions[row][column]
    
    def get_pos_for_pixels(self, x, y):
        """
        Reverse lookup for grid position based on pixels
        :param x:
        :param y:
        :return:
        """
        query_result = self.tree.query([y, x])
        if not query_result:
            raise ValueError(f"Pixel positions not found in grid! {x}, {y}")
        
        # query_result[0] - The distances to the nearest neighbour
        # query_result[1] - The locations of the neighbours
        return self.flat_pixel_positions[query_result[1]]
    
    def get_x_y_distances(self, x, y):
        """
        Get the distances for rows and columns from the given x, y pixel point.
        Used mostly by other distance calculation functions.

        :param x:
        :param y:
        :return:
        """
        y_distances = self.flat_pixel_positions[:, 0] - y
        x_distances = self.flat_pixel_positions[:, 1] - x
        
        return y_distances, x_distances
    
    def get_row_column_distances(self, row, column):
        """
        Get the distances for rows and columns from the given row, column.
        Used mostly by other distance calculation functions.
        :param row:
        :param column:
        :return:
        """
        y, x = self.get_pixel_center(row, column)
        return self.get_x_y_distances(x, y)
    
    def get_straight_line_distances(self, row, column):
        """
        Get the straight line distance from the center of the given row, column
        to all other centers in the grid.
        :param row:
        :param column:
        :return:
        """
        row_distances, column_distances = self.get_row_column_distances(row, column)
        return np.sqrt((column_distances * column_distances) + (row_distances * row_distances))
    
    def get_straight_line_distance_to_point(self, start_row, start_column, end_row, end_column):
        """
        Get the straight line distance between two grid positions centers.
        :param start_row:
        :param start_column:
        :param end_row:
        :param end_column:
        :return:
        """
        start_pixels = self.get_pixel_center(start_row, start_column)
        end_pixels = self.get_pixel_center(end_row, end_column)
        return math.sqrt((start_pixels[1] * end_pixels[1]) + (start_pixels[0] * end_pixels[0]))
    
    def get_angles(self, row, column, origin_angle):
        """
        Get the direction in degrees from the center of the given row, column
        to all other centers in the grid.
        :param row:
        :param column:
        :param origin_angle:
        :return:
        """
        row_distances, column_distances = self.get_row_column_distances(row, column)
        result = origin_angle - np.degrees(np.arctan2(row_distances, column_distances) % (2 * np.pi))
        result[np.where(result < 0)] += 360
        result[np.where(result >= 360)] -= 360
        return result
    
    def get_positions_in_fov(self, row, column, origin_angle, fov, tile_distance):
        """
        Get an indexer for grid positions that in the field of view
        from the center of the given row, column
        :param row:
        :param column:
        :param fov:
        :param tile_distance:
        :return:
        """
        straight_line_distances = self.get_straight_line_distances(row, column)
        theta = self.get_angles(row, column, origin_angle)
        half_fov = fov / 2
        
        return np.logical_and(
            np.logical_or(theta >= (360 - half_fov), theta <= half_fov),
            straight_line_distances < (self.half_tile_size * tile_distance) - self.half_tile_size
        )
