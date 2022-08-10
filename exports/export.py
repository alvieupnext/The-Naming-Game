#define the structure of an output objects, these objects will decide what output the naming game returns
class export:
  def __init__(self, name, namingGame):
    #every export object knows its own name
    self.name = name
    self.ng = namingGame

  #setup to be performed before starting the game
  def setup(self, numberOfAgents):
    pass

  #code to be performed on afterevery Iteration
  def onIteration(self, sim, it):
    pass

  #code to be performed after every simulation
  def onSimulation(self, sim):
    pass

  #code to be performed after every invention
  def onInvent(self):
    pass

  #code to be performed after every adoption
  def onAdopt(self, name, listener):
    pass

  #code to be performed after every removal
  def onRemove(self, name, agent):
    pass

  #code to be performed on picking
  def onPick(self, agent, context):
    pass

  #code to be performed on consensus
  def onConsensus(self, sim, it, consensus):
    pass

  #code to be performed on the final consensus
  def onFinalConsensus(self,sim, it):
    pass

  #code to be performed after every success
  def onSuccess(self, speaker, listener, topic, name):
    pass

  #code to be performed after every failure
  def onFailure(self, speaker, listener, intendedTopic, perceivedTopic, name):
    pass

  #code to be performed after finishing the game
  def teardown(self):
    pass

  #what has to be returned after finishing the game
  def output(self):
    pass