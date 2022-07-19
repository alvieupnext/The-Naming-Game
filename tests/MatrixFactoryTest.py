import unittest
import MatrixFactory as mf
import numpy as np

class MatrixFactoryTest(unittest.TestCase):
  #setup the test
  def setUp(self):
    #create a new asymmetrical matrix factory
    self.aFactory = mf.MatrixFactory(sym=False)
    self.sFactory = mf.MatrixFactory(sym=True)
    self.agents = 20
    self.neighbours = 4
    self.randomLinks = 5

  def test_asymCreation(self):
    """A matrix factory should be able to produce all implemented matrices"""
    lattice = self.aFactory.makeLatticeMatrix(self.agents, self.neighbours)
    scaleFree = self.aFactory.makeScaleFreeMatrix(self.agents)
    smallWorld = self.aFactory.makeSmallWorldMatrix(self.agents, self.neighbours, self.randomLinks)

  def test_symCreation(self):
    """A matrix factory should be able to produce a lower triangular matrix version of every matrix"""
    lattice = self.sFactory.makeLatticeMatrix(self.agents, self.neighbours)
    scaleFree = self.sFactory.makeScaleFreeMatrix(self.agents)
    smallWorld = self.sFactory.makeSmallWorldMatrix(self.agents, self.neighbours, self.randomLinks)
    self.assertTrue(np.allclose(lattice, np.tril(lattice)))  # check if lower triangular
    self.assertTrue(np.allclose(scaleFree, np.tril(scaleFree)))  # check if lower triangular
    self.assertTrue(np.allclose(smallWorld, np.tril(smallWorld)))  # check if lower triangular

  def test_latticeConnections(self):
    """Each agent in a lattice is connected exactly to a certain amount of neighbors"""
    asymLattice = self.aFactory.makeLatticeMatrix(self.agents, self.neighbours)
    symLattice = self.sFactory.makeLatticeMatrix(self.agents, self.neighbours)
    nonZeroRowNrs, nonZeroColumnNrs = np.nonzero(asymLattice)
    nonZeroCount = len(nonZeroRowNrs)
    # An asymmetrical lattice matrix has 20 agent *4 neighbors= 80 connections
    self.assertEqual(80, nonZeroCount)
    nonZeroRowNrsSym, nonZeroColumnNrsSym = np.nonzero(symLattice)
    nonZeroCountSym = len(nonZeroRowNrsSym)
    # The symmetrical lattice should be equal to half the asymmetrical connections (in this case 40)
    self.assertEqual(nonZeroCount / 2, nonZeroCountSym)

  def test_scaleFreeCreation(self):
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

