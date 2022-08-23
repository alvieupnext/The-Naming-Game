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
  def onIteration(self, sim, it):
    self.nameTable[it, sim] = self.inventedNames

  #reset inventedNames on every simulation
  def onSimulation(self, sim):
    self.inventedNames = 0

  #increment invented Names for every time an invent has been performed
  def onInvent(self):
    self.inventedNames += 1

  #return output
  def output(self):
    return self.nameTable

class namesInCirculation(export):

  # create a dictionary to keep track of which agents have which name in their memory
  def setup(self, numberOfAgents):
    self.circulation = {}
    self.circulationPerSim = []
    #remember consensusList
    self.consensuslist = self.ng.consensusScore
    #keep track of how many consensus scores we've passed
    self.currentConsensus = 0
    #initialize first consensus to the lowest score
    self.consensus = self.consensuslist[self.currentConsensus]
    #remember number of agents
    self.agents = numberOfAgents

  # update language circulation
  def onAdopt(self, name, listener):
    #if the list already exists
    if self.circulation.get(name):
      self.circulation[name].append(listener)
      #create new entry in the name dictionary
    else: self.circulation[name] = [listener]

  # remove agent from circulation
  def onRemove(self, name, agent):
    self.circulation[name].remove(agent)
    # if circulation list for name empty
    if not self.circulation[name]:
      #remove name entry from dictionary
      self.circulation.pop(name)

  def onSimulation(self, sim):
    #append circulation to list
    self.circulationPerSim.append(self.circulation)
    #clear circulation for the next simulation
    self.circulation = {}
    #reset current consensus and consensus value
    self.currentConsensus = 0
    # initialize first consensus to the lowest score
    self.consensus = self.consensuslist[self.currentConsensus]

  #increase consensus meter and check whether we have reached the final consensus
  def onConsensus(self, sim, it, consensus):
    # increase current consensus
    self.currentConsensus += 1
    # check whether we've reached the end
    if len(self.consensuslist) == self.currentConsensus:
      self.ng.finalConsensus = True
    else:
      self.consensus = self.consensuslist[self.currentConsensus]
      #if our new consensus proportion is still smaller than the proportion that triggered the consensus action
      if self.consensus <= consensus:
        #repeat onConsensus
        self.onConsensus(sim, it, consensus)


  #check whether we have reached an internal consensus in our code
  def checkConsensus(self, agents):
    #get proportion
    proportion = len(agents) / self.agents
    #for all names, check whether there are enough agents in the list
    if proportion >= self.consensus:
      return proportion
    else: return False

  def output(self):
    return self.circulationPerSim

  # export which generates a heatmap with the preferred action of an agent per iteration (builds on top of names in circulation)
  # preferred Action assumes every topic is the same
class preferredAction(namesInCirculation):
    # add a circulation matrix on top of the existing setup
  def setup(self, numberOfAgents):
    # perform the namesInCirculation setup
    super().setup(numberOfAgents)
    #add setup for circulation matrix
    self.circulationMatrixPerSim= []
    #remember iterations
    self.iterations = self.ng.maxIterations
    self.circulationMatrix = np.zeros((self.iterations, self.agents), dtype=object)
    # fill with empty arrays (could be shortened using Pythonism
    for x in range(self.iterations):
      for y in range(self.agents):
        self.circulationMatrix[x, y] = []

  def onSimulation(self, sim):
    #perform the namesInCirculation every Simulation
    super().onSimulation(sim)
    #append matrix to list and clear circulation matrix
    self.circulationMatrixPerSim.append(self.circulationMatrix)
    self.circulationMatrix = np.zeros((self.iterations, self.agents), dtype=object)
    #fill with empty arrays (could be shortened using Pythonism
    for x in range(self.iterations):
      for y in range(self.agents):
        self.circulationMatrix[x, y] = []

  #get the preferred action of every actor after every iteration
  def onIteration(self, sim, it):
    allNames = list(self.circulation.keys())
    for name in allNames:
      listOfAgents = self.circulation[name]
      for agent in listOfAgents:
        self.circulationMatrix[it, agent].append(name)
      #if we have reached our desired consensus, notify the Naming Game
      consensus = self.checkConsensus(listOfAgents)
      if consensus:
          self.ng.consensus = consensus


  def onFinalConsensus(self, sim, it):
    maxIterations = self.ng.maxIterations
    #fill the rest of the matrix with the last row filled in
    for i in range(it + 1, maxIterations):
      self.circulationMatrix[i, :] = self.circulationMatrix[it, :]

  #return all the circulation matrices
  def output(self):
    return self.circulationMatrixPerSim

#namePopularity assumes every topic is the same and only looks at the popularity of the name
class namePopularity(namesInCirculation):

  def setup(self, numberOfAgents):
    # perform the namesInCirculation setup
    super().setup(numberOfAgents)
    # add a new dictionary that keeps track of name popularity
    self.popularity = {}
    self.popularityPerSim = []

  #get the percentage of every used name after every iteration
  def onIteration(self, sim, it):
    allNames = list(self.circulation.keys())
    for name in allNames:
      listOfAgents = self.circulation[name]
      #calculate the proportion of how many agents know this name vs the amount of agents
      proportion = len(listOfAgents) / self.agents
      #check whether this name has appeared yet in our popularity dictionary
      if self.popularity.get(name):
        #if the name is known, add it to the list
        self.popularity[name].append(proportion)
      else:
        #if not known, generate a new list and add it to the dictionary, adding zero values for earlier iterations
        valueList = [0] * (it + 1)
        valueList[it] = proportion
        self.popularity[name] = valueList
      #if we have reached our desired consensus, notify the Naming Game
      consensus = self.checkConsensus(listOfAgents)
      if consensus:
          self.ng.consensus = consensus


  def onSimulation(self, sim):
    #perform everySimulation from parent object
    super().onSimulation(sim)
    self.popularityPerSim.append(self.popularity)
    self.popularity = {}

  def output(self):
    return self.popularityPerSim


#get iteration where simulation reaches consensus on average
class consensusIteration(export):

  def setup(self, numberOfAgents):
    #initialize consensus iteration at the maximum possible iterations
    self.consensusIteration = self.ng.maxIterations
    #create an empty consensus List
    self.consensuslist = []
    #keep a list of all the iterations where consensus was reached per simulation
    self.consensusIterationPerSim = []
    #keep track of which consensus we are on right now
    self.currentConsensus = 0

  #update consensusIteration
  def onConsensus(self, sim, it, consensus):
    #get current consensus
    currentConsensus = self.ng.consensusScore[self.currentConsensus]
    self.consensuslist.append((currentConsensus, it))
    #increase consensus count
    self.currentConsensus +=1
    #if we reached the end of our list, we reached final consensus
    if len(self.ng.consensusScore) == self.currentConsensus:
      self.ng.finalConsensus = True
    else:
      newConsensus = self.ng.consensusScore[self.currentConsensus]
      # if our new consensus proportion is still smaller than the proportion that triggered the consensus action
      if newConsensus <= consensus:
        #repeat onConsensus
        self.onConsensus(sim, it, consensus)


  #fill the consensus list at the end of every simulation
  def onSimulation(self, sim):
    self.consensusIterationPerSim.append(self.consensuslist)
    #reset consensusIteration to max
    self.consensusIteration = self.ng.maxIterations
    #reset current consensus
    self.currentConsensus = 0
    #reset current consensus list
    self.consensuslist = []

  #as output return a list of all the iterations where consensus was reached
  def output(self):
    return self.consensusIterationPerSim

#Export the amount of times an action was performed per iterations
class actionsPerformed(export):

  def setup(self, numberOfAgents):
    #initialize dictionary
    self.actions = {"invent": 0, "adopt": 0, "remove": 0, "invent": 0, "success": 0, "failure": 0, "consensusReached": 0}
    #keep a list of actions count per simulation
    self.actionsPerSim = []

  def onSimulation(self, sim):
    #update actionsPerSim list
    self.actionsPerSim.append(self.actions)
    #reset actions list
    self.actions = {"invent": 0, "adopt": 0, "remove": 0, "invent": 0, "success": 0, "failure": 0,
                    "consensusReached": 0}

  def onInvent(self):
    self.actions["invent"] += 1

  def onAdopt(self, name, listener):
    self.actions["adopt"] += 1

  def onRemove(self, name, agent):
    self.actions["remove"] += 1

  def onSuccess(self, speaker, listener, topic, name):
    self.actions["success"] += 1

  def onFailure(self, speaker, listener, intendedTopic, perceivedTopic, name):
    self.actions["failure"] += 1

  def onConsensus(self, sim, it):
    self.actions["consensusReached"] += 1

  def output(self):
    return self.actionsPerSim





possibleExports = {"names": namesInvented, "circulation": namesInCirculation, "preferredAction": preferredAction, "popularity": namePopularity, "consensus": consensusIteration,
                   "actions": actionsPerformed}
