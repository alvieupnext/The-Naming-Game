#define the structure of an output objects, these objects will decide what output the naming game returns
class export:
  def __init__(self, name):
    #every export object knows its own name
    self.name = name

  #setup to be performed before starting the game
  def setup(self, ng, numberOfAgents):
    pass

  #code to be performed on afterevery Iteration
  def everyIteration(self, sim, it):
    pass

  #code to be performed after every simulation
  def everySimulation(self, sim):
    pass

  #code to be performed after every invention
  def everyInvent(self):
    pass

  #code to be performed after every adoption
  def everyAdopt(self, name, listener):
    pass

  #code to be performed after every removal
  def everyRemove(self, name, agent):
    pass

  #code to be performed after finishing the game
  def teardown(self):
    pass

  #what has to be returned after finishing the game
  def output(self):
    pass