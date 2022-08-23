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
    #start game with lattice again (to test)
    self.singleIterationMono.start(self.lattice)

  def test_influenceBetweenSims(self):
    """The simulations in a single Naming Game are independent from each other"""
    assertFalse = self.assertFalse
    #create new subclass of BaselineNG to override setupSimulation
    class BNG(BaselineNG):
      def setupSimulation(self):
        #perform the usual setupSimulation
        super().setupSimulation()
        for memory in self.memory:
          #check that memory isn't transferred between simulations
          assertFalse(memory)
    multiSim = BNG(maxIterations=1, simulations=2, strategy=Strategy.multi, output=["actions"], display=False)
    multiSim.start(self.lattice)

  def test_inventAdopt(self):
    """The very first iteration of the Naming Game, every speaker will invent a name and both listeners will adopt"""
    #Since multi doensn't provide us with exact the same amount of agents every time, we are using mono for this test
    #Get output
    output = self.singleIterationMono.start(self.lattice)
    actions = output["actions"]
    #Single simulation
    action = actions[0]
    #Since our simulation is running one iteration, there should only be one invention and two adoptions
    self.assertEquals(1, action["invent"])
    self.assertEquals(2, action["adopt"])





