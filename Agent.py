class Agent:
    '''
    Schelling segregation agent
    '''
    # Khai bao type of agent
    typeA = 0 # Red
    typeB = 1 # Blue

    def __init__(self, id, pos, model, agent_type):
        '''
         Create a new Schelling agent.

         Args:
            id: Unique identifier for the agent.
            x, y: Agent initial location.
            type: Indicator for the agent's type (A=0, B=1)
            happy: True/False
        '''
        self.id = id
        self.pos = pos
        self.model = model
        self.type = agent_type
        self.happy = False

    def step(self):
        self.cal_happiness()

        if not self.happy: # if not happy, it move
            self.model.grid.move_to_empty(self)

    def cal_happiness(self):
        similarity = self.model.grid.get_similarity(self)
        if similarity <= self.model.similarity:
            self.happy = False
        else:
            self.happy = True
            self.model.happy += 1