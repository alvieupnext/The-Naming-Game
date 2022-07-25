from exports.export import *
import numpy as np

class namesInvented(export):

  #setup
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

possibleExports = {"names": namesInvented}
