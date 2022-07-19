import unittest
import MatrixFactory as mf
import numpy as np

class AsymmetricalTest(unittest.TestCase):
  #setup the test
  def setUp(self):
    #create a new asymmetrical matrix factory
    self.factory = mf.MatrixFactory(sym=False)
    self.agents = 20
    self.neighbours = 4
    self.randomLinks = 5

  def test_lattice(self):
    """A matrix factory should be able to produce a lattice matrix"""
    lattice = self.factory.makeLatticeMatrix(self.agents, self.neighbours)
    #An asymmetrical lattice matrix has 20*4= 80 connections
    nonZeroRowNrs, nonZeroColumnNrs = np.nonzero(lattice)
    nonZeroCount = len(nonZeroRowNrs)
    self.assertEqual(80, nonZeroCount)

  def test_scaleFree(self):
    """A matrix factory should be able to produce a scale free matrix"""
    scaleFree = self.factory.makeScaleFreeMatrix(self.agents)
    #
    nonZeroRowNrs, nonZeroColumnNrs = np.nonzero(scaleFree)
    nonZeroCount = len(nonZeroRowNrs)
    self.assertEqual(80, nonZeroCount)


if __name__ == '__main__':
  unittest.main()

# MatrixFactorySuite = unittest.TestSuite()
# MatrixFactorySuite.addTest(AsymmetricalTest())
# #create test runner
# runner = unittest.TextTestRunner()
# runner.run(MatrixFactorySuite)

