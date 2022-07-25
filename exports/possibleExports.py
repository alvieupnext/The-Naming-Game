from exports.export import *
import numpy as np

#export object that returns how many names were invented
class namesInvented(export):

  def setup(self, ng):
    #create a table for keeping track of amount of invented names
    self.nameTable = np.zeros((ng.iterations, ng.simulations))
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
  def setup(self, ng):
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


possibleExports = {"names": namesInvented, "circulation": namesInCirculation}
