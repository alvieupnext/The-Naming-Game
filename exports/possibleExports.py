from exports.export import *
import numpy as np

#export object that returns how many names were invented
class namesInvented(export):

  def setup(self, numberOfAgents):
    #create a table for keeping track of amount of invented names
    self.nameTable = np.zeros((self.ng.maxIterations, self.ng.simulations))
    #start invented names at zero
    self.inventedNames = 0

  #update the nameTable every iteration
  def everyIteration(self, sim, it):
    self.nameTable[it, sim] = self.inventedNames

  #reset inventedNames on every simulation
  def everySimulation(self, sim):
    self.inventedNames = 0

  #increment invented Names for every time an invent has been performed
  def everyInvent(self):
    self.inventedNames += 1

  #return output
  def output(self):
    return self.nameTable

class namesInCirculation(export):

  # create a dictionary to keep track of which agents have which name in their memory
  def setup(self, numberOfAgents):
    self.circulation = {}
    self.circulationPerSim = []

  # update language circulation
  def everyAdopt(self, name, listener):
    #if the list already exists
    if self.circulation.get(name):
      self.circulation[name].append(listener)
      #create new entry in the name dictionary
    else: self.circulation[name] = [listener]

  # remove agent from circulation
  def everyRemove(self, name, agent):
    self.circulation[name].remove(agent)
    # if circulation list for name empty
    if not self.circulation[name]:
      #remove name entry from dictionary
      self.circulation.pop(name)

  def everySimulation(self, sim):
    #append circulation to list
    self.circulationPerSim.append(self.circulation)
    #clear circulation for the next simulation
    self.circulation = {}

  def output(self):
    return self.circulationPerSim

  # export which generates a heatmap with the preferred action of an agent per iteration (builds on top of names in circulation)
class preferredAction(namesInCirculation):
    # add a circulation matrix on top of the existing setup
  def setup(self, numberOfAgents):
    # perform the namesInCirculation setup
    super().setup(numberOfAgents)
    #add setup for circulation matrix
    self.circulationMatrixPerSim= []
    #and consensus percent
    self.consensus = self.ng.consensusScore
    #remember number of agents
    self.numberOfAgents = numberOfAgents
    #remember iterations
    self.iterations = self.ng.maxIterations
    self.circulationMatrix = np.zeros((self.iterations, self.numberOfAgents), dtype=object)
    # fill with empty arrays (could be shortened using Pythonism
    for x in range(self.iterations):
      for y in range(self.numberOfAgents):
        self.circulationMatrix[x, y] = []

  #check whether we have reached an internal consensus in our code
  def checkConsensus(self, agents):
    #for all names, check whether there are enough agents in the list
    return len(agents) / self.numberOfAgents >= self.consensus

  def everySimulation(self, sim):
    #perform the namesInCirculation every Simulation
    super().everySimulation(sim)
    #append matrix to list and clear circulation matrix
    self.circulationMatrixPerSim.append(self.circulationMatrix)
    self.circulationMatrix = np.zeros((self.iterations, self.numberOfAgents), dtype=object)
    #fill with empty arrays (could be shortened using Pythonism
    for x in range(self.iterations):
      for y in range(self.numberOfAgents):
        self.circulationMatrix[x, y] = []

  #get the preferred action of every actor after every iteration
  def everyIteration(self, sim, it):
    allNames = list(self.circulation.keys())
    for name in allNames:
      listOfAgents = self.circulation[name]
      for agent in listOfAgents:
        self.circulationMatrix[it, agent].append(name)
      #if we have reached our desired consensus, notify the Naming Game
      if self.checkConsensus(listOfAgents):
        self.ng.consensus = True



  #return all the circulation matrices
  def output(self):
    return self.circulationMatrixPerSim





possibleExports = {"names": namesInvented, "circulation": namesInCirculation, "preferredAction": preferredAction}
