# -*- coding: utf-8 -*-
"""
Mesa Space Module
=================

Objects used to add a spatial component to a model.

Grid: base grid, a simple list-of-lists.
SingleGrid: grid which strictly enforces one object per cell.
"""
# Instruction for PyLint to suppress variable name errors, since we have a
# good reason to use one-character variable names for x and y.
# pylint: disable=invalid-name

import itertools
import random
import math

# def accept_tuple_argument(wrapped_function):
#     """ Decorator to allow grid methods that take a list of (x, y) position tuples
#     to also handle a single position, by automatically wrapping tuple in
#     single-item list rather than forcing user to do it.
#
#     """
#     def wrapper(*args):
#         if isinstance(args[1], tuple) and len(args[1]) == 2:
#             return wrapped_function(args[0], [args[1]])
#         else:
#             return wrapped_function(*args)
#     return wrapper

class Grid:
    """ Base class for a square grid.

    Grid cells are indexed by [x][y], where [0][0] is assumed to be the
    bottom-left and [width-1][height-1] is the top-right. If a grid is
    toroidal, the top and bottom, and left and right, edges wrap to each other

    Properties:
        width, height: The grid's width and height.
        grid: Internal list-of-lists which holds the grid cells themselves.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
        get_neighborhood: Returns the cells surrounding a given cell.
        get_cell_list_contents: Returns the contents of a list of cells
            ((x,y) tuples)
        neighbor_iter: Iterates over position neightbors.
        coord_iter: Returns coordinates as well as cell contents.
        place_agent: Positions an agent on the grid, and set its pos variable.
        move_agent: Moves an agent from its current position to a new position.
        iter_neighborhood: Returns an iterator over cell coordinates that are
        in the neighborhood of a certain point.
        torus_adj: Converts coordinate, handles torus looping.
        out_of_bounds: Determines whether position is off the grid, returns
        the out of bounds coordinate.
        iter_cell_list_contents: Returns an iterator of the contents of the
        cells identified in cell_list.
        get_cell_list_contents: Returns a list of the contents of the cells
        identified in cell_list.
        remove_agent: Removes an agent from the grid.
        is_cell_empty: Returns a bool of the contents of a cell.

    """
    def __init__(self, height, width):
        """ Create a new grid.

        Args:
            width, height: The width and height of the grid

        """
        self.height = height
        self.width = width

        self.grid = []

        for x in range(self.height):
            col = []
            for y in range(self.width):
                col.append(self.default_val()) # None
            self.grid.append(col)

        # Add all cells to the empties list: cac cap toa do
        self.empties = list(itertools.product(*(range(self.height), range(self.width))))

    @staticmethod
    def default_val():
        """ Default value for new cell elements. """
        return None

    def __getitem__(self, index):
        return self.grid[index]

    # def __len__(self):
    #     return self.height * self.width

#    def __iter__(self):
        # create an iterator that chains the
        #  rows of grid together as if one list:
#        return itertools.chain(*self.grid)


    # def neighbors_iter(self, pos):
    #     """ Iterate over position neighbors.
    #
    #     Args:
    #         pos: (x,y) coords tuple for the position to get the neighbors of.
    #         moore: Boolean for whether to use Moore neighborhood (including
    #                diagonals) or Von Neumann (only up/down/left/right).
    #
    #     """
    #     neighborhood = self.iter_neighborhood(pos)
    #     return self.iter_cell_list_contents(neighborhood)

    def get_similarity(self, agent):
        neighbors = self._get_neighborhood(agent.pos)
        num_neighbors = len(neighbors)
        similar = 0
        for neighbor in neighbors:
            agent_neighbor = self[neighbor[0]][neighbor[1]]
            if not self._is_cell_empty(neighbor) and agent_neighbor.type == agent.type:
                similar += 1
        return (float)(similar) / num_neighbors


#
#     def iter_neighbors(self, pos, moore,
#                        include_center=False, radius=1):
#         """ Return an iterator over neighbors to a certain point.
#
#         Args:
#             pos: Coordinates for the neighborhood to get.
#             moore: If True, return Moore neighborhood
#                     (including diagonals)
#                    If False, return Von Neumann neighborhood
#                      (exclude diagonals)
#             include_center: If True, return the (x, y) cell as well.
#                             Otherwise,
#                             return surrounding cells only.
#             radius: radius, in cells, of neighborhood to get.
#
#         Returns:
#             An iterator of non-None objects in the given neighborhood;
#             at most 9 if Moore, 5 if Von-Neumann
#             (8 and 4 if not including the center).
#
#         """
#         neighborhood = self.iter_neighborhood(
#             pos, moore, include_center, radius)
#         return self.iter_cell_list_contents(neighborhood)
#
#     def get_neighbors(self, pos, moore,
#                       include_center=False, radius=1):
#         """ Return a list of neighbors to a certain point.
#
#         Args:
#             pos: Coordinate tuple for the neighborhood to get.
#             moore: If True, return Moore neighborhood
#                     (including diagonals)
#                    If False, return Von Neumann neighborhood
#                      (exclude diagonals)
#             include_center: If True, return the (x, y) cell as well.
#                             Otherwise,
#                             return surrounding cells only.
#             radius: radius, in cells, of neighborhood to get.
#
#         Returns:
#             A list of non-None objects in the given neighborhood;
#             at most 9 if Moore, 5 if Von-Neumann
#             (8 and 4 if not including the center).
#
#         """
#         return list(self.iter_neighbors(
#             pos, moore, include_center, radius))
#
#     '''
#     def torus_adj(self, coord, dim_len):
#         """ Convert coordinate, handling torus looping. """
#         if self.torus:
#             coord %= dim_len
#         return coord
#     '''



    # @accept_tuple_argument
    # def iter_cell_list_contents(self, cell_list):
    #     """
    #     Args:
    #         cell_list: Array-like of (x, y) tuples, or single tuple.
    #
    #     Returns:
    #         An iterator of the contents of the cells identified in cell_list
    #
    #     """
    #     return (self[x][y] for x, y in cell_list if not self._is_cell_empty((x, y)))

#     @accept_tuple_argument
#     def get_cell_list_contents(self, cell_list):
#         """
#         Args:
#             cell_list: Array-like of (x, y) tuples, or single tuple.
#
#         Returns:
#             A list of the contents of the cells identified in cell_list
#
#         """
#         return list(self.iter_cell_list_contents(cell_list))
#
#     def move_agent(self, agent, pos):
#         """
#         Move an agent from its current position to a new position.
#
#         Args:
#             agent: Agent object to move. Assumed to have its current location
#                    stored in a 'pos' tuple.
#             pos: Tuple of new position to move the agent to.
#
#         """
#         self._remove_agent(agent.pos, agent)
#         self._place_agent(pos, agent)
#         agent.pos = pos
#
#     def place_agent(self, agent, pos):
#         """ Position an agent on the grid, and set its pos variable. """
#         self._place_agent(pos, agent)
#         agent.pos = pos
#

#
#     def remove_agent(self, agent):
#         """ Remove the agent from the grid and set its pos variable to None. """
#         pos = agent.pos
#         self._remove_agent(pos, agent)
#         agent.pos = None
#


    # def is_cell_empty(self, pos):
    #     """ Returns a bool of the contents of a cell. """
    #     x, y = pos
    #     return True if self.grid[x][y] == self.default_val() else False

    def move_to_empty(self, agent):
        """ Moves agent to a random empty cell, vacating agent's old cell. """
        pos = agent.pos
        new_pos = self._find_empty()
        if new_pos is None:
            raise Exception("ERROR: No empty cells")
        else:
            self._place_agent(new_pos, agent)
            agent.pos = new_pos
            self._remove_agent(pos, agent)

    # def find_empty(self):
    #      """ Pick a random empty cell. """
    #      if self.exists_empty_cells():
    #          pos = random.choice(self.empties)
    #          return pos
    #      else:
    #          return None

    # def exists_empty_cells(self):
    #      """ Return True if any cells empty else False. """
    #      return len(self.empties) > 0

    # def position_agent(self, agent):
    #     coords = self.find_empty()
    #     if coords is None:
    #         raise Exception("ERROR: Grid full")
    #     agent.pos = coords
    #     if self.is_cell_empty(agent.pos):
    #         self._place_agent(agent.pos, agent)
    #     else:
    #         raise Exception("Cell not empty")

    def add_agent(self, agent):
        # Lay mot o trong bat ky
        # Gan agent vao o trong do
        coords = self._find_empty()
        if coords is None:
            raise Exception("ERROR: Grid full")
        agent.pos = coords
        if self._is_cell_empty(agent.pos):
            self._place_agent(agent.pos, agent)
        else:
            raise Exception("Cell not empty")

    def coord_iter(self):
        """ An iterator that returns coordinates as well as cell contents. """
        for row in range(self.height):
            for col in range(self.width):
                yield self.grid[row][col], row, col    # agent, x, y

    def _out_of_bounds(self, pos):
        """
        Determines whether position is off the grid, returns the out of
        bounds coordinate.
        """
        x, y = pos
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def _find_empty(self):
         """ Pick a random empty cell. """
         if self._exists_empty_cells():
             pos = random.choice(self.empties)
             return pos
         else:
             return None

    def _exists_empty_cells(self):
         """ Return True if any cells empty else False. """
         return len(self.empties) > 0

    def _is_cell_empty(self, pos):
        """ Returns a bool of the contents of a cell. """
        x, y = pos
        return True if self.grid[x][y] == self.default_val() else False

    def _place_agent(self, pos, agent):
         """ Place the agent at the correct location. """
         x, y = pos
         self.grid[x][y] = agent
         if pos in self.empties:
             self.empties.remove(pos)

    def _remove_agent(self, pos, agent):
        """ Remove the agent from the given location. """
        x, y = pos
        self.grid[x][y] = None
        self.empties.append(pos)

    def _iter_neighborhood(self, pos):
        x, y = pos
        coordinates = set()
        for dy in range(-1,  2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue

                px = x + dx
                py = y + dy

                # Skip if new coords out of bounds.
                if(self._out_of_bounds((px, py))):
                    continue

                coords = (px, py)
                if coords not in coordinates:
                    coordinates.add(coords)
                    yield coords

    def _get_neighborhood(self, pos):
        """ Return a list of cells that are in the neighborhood of a
        certain point.

        Args:
            pos: Coordinate tuple for the neighborhood to get.

        Returns:
            A list of coordinate tuples representing the neighborhood
        """
        return list(self._iter_neighborhood(pos))