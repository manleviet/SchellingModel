from random import randint
import datetime as dt
from Grid import Grid

#from mesa.time import RandomActivation
#from mesa.datacollection import DataCollector

class SchellingAgent:
    '''
    Schelling segregation agent
    '''
    def __init__(self, unique_id, pos, model, agent_type):
        '''
         Create a new Schelling agent.

         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agent's type (A=0, B=1)
        '''
        self.unique_id = unique_id
        self.pos = pos
        self.model = model
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.neighbors(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move:
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1

class SchellingModel:
    '''
    Model class for the Schelling segregation model.
    '''

    def __init__(self, width, height, density):
        self.width = width
        self.height = height
        num_agent = (int)(height * width * density / 2)

        #self.schedule = RandomActivation(self)
        self.grid = Grid(width, height)

        self.happy = 0
        '''
        self.datacollector = DataCollector(
            {"happy": lambda m: m.happy},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
        '''
        self.running = True

        # if seed is None:
        #     self.seed = dt.datetime.now()
        # else:
        #     self.seed = seed
        # random.seed(seed)
        # self.running = True
        # self.schedule = None

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for i in range(0, num_agent):
            agent = SchellingAgent(i, (0, 0), self, 0)
            self.grid.position_agent(agent)
            # self.schedule.add(agent)

        for i in range(0, num_agent):
            agent = SchellingAgent(i, (0, 0), self, 1)
            self.grid.position_agent(agent)
            # self.schedule.add(agent)

    # def step(self):
    #     '''
    #     Run one step of the model. If All agents are happy, halt the model.
    #     '''
    #     self.happy = 0  # Reset counter of happy agents
    #     self.schedule.step()
    #     self.datacollector.collect(self)
    #
    #     if self.happy == self.schedule.get_agent_count():
    #         self.running = False

model = SchellingModel(5, 5, 0.8)
for cell in model.grid.coord_iter():
    agent = cell[0]
    x = cell[1]
    y = cell[2]
    if agent == None:
        agent_type = -1
    else:
        agent_type = agent.type
    print('{} {} {}'.format(x, y, agent_type))