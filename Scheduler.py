import random

class BaseScheduler:
    """ Simplest scheduler; activates agents one at a time, in the order
    they were added.

    Assumes that each agent added has a *step* method which takes no arguments.

    (This is explicitly meant to replicate the scheduler in MASON).

    """
    model = None
    agents = []

    def __init__(self, model):
        """ Create a new, empty BaseScheduler. """
        self.model = model
        self.agents = []

    def add(self, agent):
        """ Add an Agent object to the schedule.

        Args:
            agent: An Agent to be added to the schedule. NOTE: The agent must
            have a step() method.

        """
        self.agents.append(agent)

    def remove(self, agent):
        """ Remove all instances of a given agent from the schedule.

        Args:
            agent: An agent object.

        """
        while agent in self.agents:
            self.agents.remove(agent)

    def step(self):
        """ Execute the step of all the agents, one at a time. """
        for agent in self.agents[:]:
            agent.step()

    def get_agent_count(self):
        """ Returns the current number of agents in the queue. """
        return len(self.agents)

class RandomActivation(BaseScheduler):
    """ A scheduler which activates each agent once per step, in random order,
    with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask agents...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step(model) method.

    """
    def step(self):
        """ Executes the step of all agents, one at a time, in
        random order.

        """
        random.shuffle(self.agents)
        for agent in self.agents[:]:
            agent.step()