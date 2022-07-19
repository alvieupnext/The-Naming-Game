import unittest
import MatrixFactory as mf
import numpy as np

class MatrixFactoryTest(unittest.TestCase):
  #setup the test
  def setUp(self):
    #create a new asymmetrical matrix factory
    self.aFactory = mf.MatrixFactory(sym=False)
    self.sFactory = mf.MatrixFactory(sym=True)

  def test_asymCreation(self):
    """A matrix factory should be able to produce all implemented matrices"""
    lattice = self.aFactory.makeLatticeMatrix(20, 4)
    scaleFree = self.aFactory.makeScaleFreeMatrix(10)
    smallWorld = self.aFactory.makeSmallWorldMatrix(15, 5, 4)

  def test_symCreation(self):
    """A matrix factory should be able to produce a lower triangular matrix version of every matrix"""
    lattice = self.sFactory.makeLatticeMatrix(20, 4)
    scaleFree = self.sFactory.makeScaleFreeMatrix(10)
    smallWorld = self.sFactory.makeSmallWorldMatrix(15, 5, 4)
    self.assertTrue(np.allclose(lattice, np.tril(lattice)))  # check if lower triangular
    self.assertTrue(np.allclose(scaleFree, np.tril(scaleFree)))  # check if lower triangular
    self.assertTrue(np.allclose(smallWorld, np.tril(smallWorld)))  # check if lower triangular

  def test_latticeConnections(self):
    """Each agent in a lattice is connected exactly to a certain amount of neighbors"""
    def doTest(pair):
      agents = pair[0]
      neighbours = pair[1]
      asymLattice = self.aFactory.makeLatticeMatrix(agents, neighbours)
      symLattice = self.sFactory.makeLatticeMatrix(agents, neighbours)
      nonZeroRowNrs, nonZeroColumnNrs = np.nonzero(asymLattice)
      nonZeroCount = len(nonZeroRowNrs)
      # An asymmetrical lattice matrix has 20 agent *4 neighbors= 80 connections
      print(asymLattice)
      self.assertEqual(agents*neighbours, nonZeroCount, "Asymmetrical Error")
      nonZeroRowNrsSym, nonZeroColumnNrsSym = np.nonzero(symLattice)
      nonZeroCountSym = len(nonZeroRowNrsSym)
      # The symmetrical lattice should be equal to half the asymmetrical connections (in this case 40)
      self.assertEqual(agents*neighbours / 2, nonZeroCountSym, "Symmetrical Error")
      ##ASK ABOUT UNEVEN NEIGHBOURS
    latticePairs = [(20,4), (30,6), (99, 4), (15,10)]

    for pair in latticePairs:
      doTest(pair)

  def test_scaleFreeConnections(self):
    """A matrix factory should be able to produce a scale free matrix"""
    scaleFree = self.aFactory.makeScaleFreeMatrix(self.agents)
    #
    nonZeroRowNrs, nonZeroColumnNrs = np.nonzero(scaleFree)
    nonZeroCount = len(nonZeroRowNrs)
    #expected non zero elements = 8 (starting connections from 4 agents) + 2 (two-way connection) * Established Links (default 2) * 16 (agents - 4) = 72
    self.assertEqual(72, nonZeroCount)

  def test_scaleFreeLinks(self):
    """A scale free matrix should have a certain amount of connections depending """



if __name__ == '__main__':
  unittest.main()

