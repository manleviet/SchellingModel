from random import randint
import datetime as dt
from Grid import Grid
from Scheduler import RandomActivation
import matplotlib.pyplot as plt

#from mesa.datacollection import DataCollector

class Agent:
    '''
    Schelling segregation agent
    '''
    # Khai bao type of agent
    typeA = 0
    typeB = 1

    def __init__(self, id, pos, model, agent_type):
        '''
         Create a new Schelling agent.

         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            type: Indicator for the agent's type (A=0, B=1)
        '''
        self.id = id
        self.pos = pos
        self.model = model
        self.type = agent_type

    def step(self):
        similarity = self.model.grid.get_similarity(self)

        # If unhappy, move:
        if similarity <= self.model.similarity:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1

class Model:
    '''
    Model class for the Schelling segregation model.
    '''

    def __init__(self, width, height, density, similarity):
        self.width = width
        self.height = height
        num_agent = (int)(height * width * density / 2)
        self.similarity = similarity

        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width)

        self.happy = 0
        '''
        self.datacollector = DataCollector(
            {"happy": lambda m: m.happy},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
        '''
        self.running = True

        # Set up agents
        id = 0
        id = self._create_agent(id, num_agent, Agent.typeA)
        id = self._create_agent(id, num_agent, Agent.typeB)

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
        #self.print_grid()
        self.plot_grid()
        #self.datacollector.collect(self)

        print(self.happy)
        if self.happy == self.schedule.get_agent_count():
            self.running = False

    def print_grid(self):
        for cell in self.grid.coord_iter():
            agent = cell[0]
            x = cell[1]
            y = cell[2]
            if agent == None:
                agent_type = -1
            else:
                agent_type = agent.type
            print '{}  '.format(agent_type),
            if y == model.width - 1:
                print('\n')

    def plot_grid(self):
        plt.plot(self.grid)
        plt.show()

model = Model(100, 100, 0.8, 0.5)

#model.print_grid()

for i in range(20):
    model.step()