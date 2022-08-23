import unittest
from variants.BaselineNG import *
import Strategy
from MatrixFactory import *
from exports.export import *

class NamingGameTest(unittest.TestCase):
  #setup the Naming Game (using actions export) for games that only
  def setUp(self):
    self.singleIterationMono = BaselineNG(maxIterations=1, simulations=1, strategy=Strategy.mono, output=["actions"], display=False)
    self.singleIterationMulti = BaselineNG(maxIterations=1, simulations=1, strategy=Strategy.multi, output=["actions"], display=False)
    self.singleItMultSim = BaselineNG(maxIterations=1, simulations=2, strategy=Strategy.multi, output=["actions"], display=False)
    self.numberOfAgents = 5
    self.lattice = MatrixFactory().makeLatticeMatrix(self.numberOfAgents, 2)

  def test_startEmptyMemory(self):
    """Prior to starting a new Naming Game, every agent has no previous memory of the previous game"""
    #create an output test object that checks whether we have empty memory at the start and between simulations
    outputTest = export("test", self.singleIterationMono)
    def testEveryAgent(noOfAgents):
      for i in range(noOfAgents):
        self.assertFalse(outputTest.ng.memory[i])
    outputTest.setup = testEveryAgent
    #add this output object to singleIterationMono
    self.singleIterationMono.output.append(outputTest)
    #start game with lattice
    self.singleIterationMono.start(self.lattice)



