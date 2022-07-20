import unittest
import MatrixFactory as mf
import AgentPairs as ap

class AgentPairsTest(unittest.TestCase):
  #setup test
  def setUp(self):
    rFactory = mf.MatrixFactory(triangular=False)
    tFactory = mf.MatrixFactory(triangular=True)
    randomFactory = mf.MatrixFactory(triangular=True)
    #using lattices since they involve no random chances
    self.rlattice = rFactory.makeLatticeMatrix(20,4)
    self.tlattice = tFactory.makeLatticeMatrix(20,4)
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
      self.assertTrue(a and b not in seen, "symmetrical")
      seen.append(a)
      seen.append(b)
    tPairs = self.pair.generate(self.tlattice)
    seen = []
    for a, b in tPairs:
      self.assertNotEqual(a, b)
      self.assertTrue(a and b not in seen, "asymmetrical")
      seen.append(a)
      seen.append(b)

