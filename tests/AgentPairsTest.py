import unittest
import MatrixFactory as mf
import AgentPairs as ap
import numpy as np

class AgentPairsTest(unittest.TestCase):
  #setup test
  def setUp(self):
    rFactory = mf.MatrixFactory(triangular=False)
    tFactory = mf.MatrixFactory(triangular=True)
    #using lattices since they involve no random chances
    self.rlattice = rFactory.makeLatticeMatrix(20,4)
    self.tlattice = tFactory.makeLatticeMatrix(20,4)
    self.weightedMatrix = np.array([[0,3,0], [2, 0, 1], [5, 3, 0]])
    self.pair = ap.AgentPairs()

  def test_pairCreation(self):
    """An AgentPair object can generate pairs from a matrix, either using the library's method or Villatoro method"""
    #VillatoroMethod
    self.pair.generateVillatoro(self.rlattice)
    self.pair.generateVillatoro(self.tlattice)
    #OurMethod
    self.pair.generate(self.rlattice)
    self.pair.generate(self.tlattice)

  #I'm not further testing the Villatoro Method since there is a lot to unpack there and I'm not sure if we are going to need this method

  def test_uniquePartner(self):
    """Generated pairs should be unique and not further connected with another agent"""
    rPairs = self.pair.generate(self.rlattice)
    seen = []
    for a, b in rPairs:
      self.assertNotEqual(a, b)
      self.assertTrue(a not in seen and b not in seen, "symmetrical: " + str(a) + " and " + str(b) + "in" + str(seen))
      seen.append(a)
      seen.append(b)
    tPairs = self.pair.generate(self.tlattice)
    seen = []
    for a, b in tPairs:
      self.assertNotEqual(a, b)
      self.assertTrue(a and b not in seen, "asymmetrical")
      seen.append(a)
      seen.append(b)

  def test_genuineConnections(self):
    """All formed agent pairs have a connection with eachother in the matrix"""
    tPairs = self.pair.generate(self.rlattice)
    for a, b in tPairs:
      self.assertEqual(1, self.rlattice[a,b])

  def test_pairLimit(self):
    """There are at most numberOfAgents divided by 2 pairs formed"""
    tPairs = self.pair.generate(self.rlattice)
    self.assertLessEqual(len(tPairs), 10)

  def test_uniquePartnerWeighted(self):
    """In a weighted agent pairing, generated pairs should be unique and not further connected with another agent"""
    pairs = self.pair.generateWeighted(self.weightedMatrix)
    seen = []
    for a, b in pairs:
      self.assertNotEqual(a, b)
      self.assertTrue(a not in seen and b not in seen, "symmetrical: " + str(a) + " and " + str(b) + "in" + str(seen))
      seen.append(a)
      seen.append(b)


