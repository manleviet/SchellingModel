import itertools
import random
import matplotlib.pyplot as plt

class Grid:
    plot_cell_size = 20

    def __init__(self, height, width):
        """ Create a new grid.
        Args:
            width, height: The width and height of the grid
        """
        self.height = height
        self.width = width

        self.grid = []
        for x in range(self.height):
            row = []
            for y in range(self.width):
                row.append(self.default_val()) # None
            self.grid.append(row)

        # empties luu tru cac cap toa do tai do cell la rong (None)
        self.empties = list(itertools.product(*(range(self.height), range(self.width))))

    @staticmethod
    def default_val():
        """ Default value for new cell elements. """
        return None

    def get_similarity(self, agent):
        neighbors = self._get_neighborhood(agent.pos)
        num_neighbors = len(neighbors)
        similar = 0
        for neighbor in neighbors:
            agent_neighbor = self.grid[neighbor[0]][neighbor[1]]
            if not self._is_cell_empty(neighbor) and agent_neighbor.type == agent.type:
                similar += 1
        return (float)(similar) / num_neighbors

    def cal_happiness(self):
        for row in range(self.height):
            for col in range(self.width):
                agent = self.grid[row][col]
                if agent != None:
                    agent.cal_happiness()

    def plot_happiness(self, happy, filename):
        for row in range(self.height):
            for col in range(self.width):
                agent = self.grid[row][col]

                color = 'black'
                if agent != None and agent.happy:
                    color = 'red'

                rectangle = plt.Rectangle((row * self.plot_cell_size, col * self.plot_cell_size),
                                          self.plot_cell_size, self.plot_cell_size, fc=color, ec='black')
                plt.gca().add_patch(rectangle)
        plt.title('Happy: {}'.format(happy))
        plt.axis('scaled')

        plt.savefig(filename)

    def plot_grid(self, happy, savefile=False, filename=None):
        for row in range(self.height):
            for col in range(self.width):
                agent = self.grid[row][col]

                if agent == None:
                    color = 'black'
                else:
                    if agent.type == 0:
                        color = 'red'
                    else:
                        color = 'blue'

                rectangle = plt.Rectangle((row * self.plot_cell_size, col * self.plot_cell_size),
                                          self.plot_cell_size, self.plot_cell_size, fc=color, ec='black')
                plt.gca().add_patch(rectangle)

        plt.title('Happy: {}'.format(happy))
        plt.axis('scaled')

        if savefile:
            plt.savefig(filename)
        else:
            plt.show()

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