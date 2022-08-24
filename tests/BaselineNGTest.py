import unittest
from variants.BaselineNG import *
import Strategy
from MatrixFactory import *
from exports.export import *
import numpy as np

class NamingGameTest(unittest.TestCase):
  #setup the Naming Game (using actions export) for games that only
  def setUp(self):
    self.singleIterationMono = BaselineNG(maxIterations=1, simulations=1, strategy=Strategy.mono, output=["actions", "memory"], display=False)
    self.singleIterationMulti = BaselineNG(maxIterations=1, simulations=1, strategy=Strategy.multi, output=["actions"], display=False)
    self.singleItMultSim = BaselineNG(maxIterations=1, simulations=2, strategy=Strategy.multi, output=["actions"], display=False)
    self.multiIT = BaselineNG(maxIterations=2, simulations=1, strategy=Strategy.multi, output=["actions"], display=True)
    self.numberOfAgents = 5
    self.lattice = MatrixFactory().makeLatticeMatrix(self.numberOfAgents, 2)
    self.singleConnection = np.array([[0,1],[1,0]])

  def test_adopt(self):
    """An agent will store a name in memory when adopting"""
    #Run a single first iteration which should invent a name adopted by both parties
    output = self.singleIterationMono.start(self.singleConnection)
    memories = output["memory"]
    #single simulation
    memory = memories[0]
    agent0 = memory[0]
    agent1 = memory[1]
    #check that the memories aren't empty
    self.assertTrue(agent0)
    self.assertTrue(agent1)
    #check that both parties agree on the same name and topic
    for pair0, pair1 in zip(agent0, agent1):
      self.assertEqual(pair0[0], pair1[0])
      self.assertEqual(pair0[1], pair1[1])






