from Grid import Grid
from Scheduler import RandomActivation
from Agent import Agent

class Model:
    '''
    Model class for the Schelling segregation model.
    '''

    def __init__(self, width, height, density, similarity):
        self.width = width
        self.height = height
        num_agent = (int)(height * width * density / 2) # so agent moi loai, chua ra 20% empty cell
        self.similarity = similarity # muc do tuong tu

        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width)

        self.happy = 0
        self.running = True

        # Set up agents
        id = 0
        id = self._create_agent(id, num_agent, Agent.typeA)
        id = self._create_agent(id, num_agent, Agent.typeB)
        self.grid.cal_happiness() # tinh initial happiness

    def _create_agent(self, startid, num, type):
        id = startid
        for i in range(0, num):
            agent = Agent(id, (0, 0), self, type)
            id = id + 1
            self.grid.add_agent(agent)
            self.schedule.add(agent)
        return id

    def step(self):
        '''
        Run one step of the model. If All agents are happy, halt the model.
        '''
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()

        if self.happy == self.schedule.get_agent_count():
            self.running = False

    def plot_grid(self, savefile=False, filename=None):
        self.grid.plot_grid(self.happy, savefile, filename)

    def plot_happiness(self, filename):
        self.grid.plot_happiness(self.happy, filename)

    def is_happy(self): # model da happy roi thi dung lai
        return not self.running

    # it's just for test purpose
    def print_grid(self):
        for cell in self.grid.coord_iter():
            agent = cell[0]
            y = cell[2]
            if agent == None:
                agent_type = -1
            else:
                agent_type = agent.type
            print '{}  '.format(agent_type),
            if y == self.width - 1:
                print('\n')