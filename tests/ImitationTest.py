import unittest
from variants.Imitation import *
import Strategy
from MatrixFactory import *
import numpy as np

class ImitationTest(unittest.TestCase):
  #
  def strategy(self, agents):
    #we will first return [[1, 2] [0, 4]] to get two names invented
    #then we will make 1 and 0 interact to trigger the behavior we want
    if self.step:
      self.step = 0
      return [[1, 0]]
    else:
      self.step += 1
      return [[1, 2], [0, 4]]

  def setUp(self):
    self.step = 0
    self.imi = Imitation(maxIterations=2, simulations=1, strategy=self.strategy, output=["actions", "memory"], display=True)
    self.imi2 = Imitationv2(maxIterations=2, simulations=1, strategy=self.strategy, output=["actions", "memory"], display=True)
    self.imi2_3 = Imitationv2(maxIterations=3, simulations=1, strategy=self.strategy, output=["actions", "memory"])
    self.numberOfAgents = 5
    self.lattice = MatrixFactory().makeLatticeMatrix(self.numberOfAgents, 2)

  def test_adoptRemove(self):
    """When confronted with a different name for the same topic, the listener will remove all previous instances of that topic and will only use the new name for the topic"""
    output = self.imi.start(self.lattice)
    actions = output["actions"]
    #single simulation
    action = actions[0]
    #check how many times a name was removed (should be one)
    self.assertEqual(1, action["remove"])
    memories = output["memory"]
    memory = memories[0]
    #check whether agent 0 and agent 1 have the same name for all topics
    agent0 = memory[0]
    agent1 = memory[1]
    for pair0, pair1 in zip(agent0, agent1):
      if (pair0[1] == pair1[1]):
        self.assertEqual(pair0[0], pair1[0])
    #check whether agent 4 and agent 1 have different names for the same topic (since they haven't interacted)
    agent4 = memory[4]
    for pair0, pair4 in zip(agent0, agent4):
      if (pair0[1] == pair4[1]):
        self.assertNotEqual(pair0[0], pair4[0])

  def test_multipleAdoption(self):
    """In The v2 Imitation, an agent is capable of adapting several different names for the same topic"""
    output = self.imi2.start(self.lattice)
    actions = output["actions"]
    # single simulation
    action = actions[0]
    # check how many times a name was removed (should be zero)
    self.assertEqual(0, action["remove"])
    memories = output["memory"]
    memory = memories[0]
    # check the length of agent 0
    agent0 = memory[0]
    #check how many memory entries agent 0 has (should be 2)
    self.assertEqual(2, len(agent0))
    #check that the memory entries have the same topic
    entry1, entry2 = agent0
    #get topic (on index 1)
    self.assertEqual(entry1[1], entry2[1])

  def test_successRemove(self):
    """In The v2 Imitation, an agent only removes multiple names of a topic when it reaches success in an iteration """
    output = self.imi2_3.start(self.lattice)
    actions = output["actions"]
    # single simulation
    action = actions[0]
    # check how many times a name was removed (should be one)
    self.assertEqual(1, action["remove"])
    memories = output["memory"]
    memory = memories[0]
    # check the length of agent 0
    agent0 = memory[0]
    self.assertEqual(1, len(agent0))
    # check whether agent 0 and agent 1 have the same name for all topics
    agent0 = memory[0]
    agent4 = memory[4]
    for pair0, pair4 in zip(agent0, agent4):
      if (pair0[1] == pair4[1]):
        self.assertEqual(pair0[0], pair4[0])