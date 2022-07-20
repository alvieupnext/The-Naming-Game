import unittest
import MatrixFactory as mf
import AgentPairs as ap

class AgentPairsTest(unittest.TestCase):
  #setup test
  def setUp(self):
    rFactory = mf.MatrixFactory(triangular=False, random=1000)
    tFactory = mf.MatrixFactory(triangular=True, random=1000)
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
    self.pair.generate(self.rlattice, symmetrical=True)
    self.pair.generate(self.tlattice, symmetrical=False)

  #I'm not further testing the Villatoro Method since there is a lot to unpack there and I'm not sure if we are going to need this method

  def test_uniquePartner(self):
    """Generated pairs should be unique and not further connected with another agent"""
    rPairs = self.pair.generate(self.tlattice, symmetrical=True)
    seen = []
    for pair in rPairs:
      a = pair[0]
      b = pair[1]
      self.assertNotEqual(a, b)
      self.assertTrue(a not in seen and b not in seen)
      seen.append(a)
      seen.append(b)