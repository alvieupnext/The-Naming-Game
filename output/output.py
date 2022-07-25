from abc import ABC, abstractmethod
#define the structure of an output objects, these objects will decide what output the naming game returns
class output(ABC):
  #setup to be performed before starting the game
  @abstractmethod
  def setup(self, ng):
    pass

  #code to be performed on afterevery Iteration
  @abstractmethod
  def everyIteration(self, ng, sim, it):
    pass

  #code to be performed after every simulation
  @abstractmethod
  def everySimulation(self, ng, sim):
    pass

  #code to be performed after finishing the game
  def teardown(self, ng):
    pass

  #what has to be returned after finishing the game
  @abstractmethod
  def output(self, ng):
    pass