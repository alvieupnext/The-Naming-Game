import unittest
from namingGameTools import AgentPairs as ap, MatrixFactory as mf
import numpy as np
# importing the module
import collections

class AgentPairsTest(unittest.TestCase):
  #setup test
  def setUp(self):
    rFactory = mf.MatrixFactory(triangular=False)
    tFactory = mf.MatrixFactory(triangular=True)
    #using lattices since they involve no random chances
    self.rlattice = rFactory.makeLatticeMatrix(20,4)
    self.tlattice = tFactory.makeLatticeMatrix(20,4)
    self.weightedMatrix = np.array([[0,3,0, 2], [2, 0, 1, 2], [6, 20, 0, 4], [0, 0, 60, 0]])
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
    print(pairs)
    seen = []
    for a, b in pairs:
      self.assertNotEqual(a, b)
      self.assertTrue(a not in seen and b not in seen)
      seen.append(a)
      seen.append(b)

  def test_weight(self):
    """In a weighted agent pairing, certain agent pairs should be more likely to return than others"""
    #get all non zero elements from the weighted matrix
    nonZero = np.nonzero(self.weightedMatrix)
    #transpose to get row column pairs
    nonZeroIdx = np.transpose(nonZero)
    #get all non zero values, get the weight
    weights = self.weightedMatrix[nonZero]
    #get sum of all weight
    totalWeight = sum(weights)
    #generate pair with the row column string and weight
    weightPairs = []
    for index, weight in zip(nonZeroIdx, weights):
      weightPairs.append((str(index), weight))
    #generate an agent pair iteration amount of times
    iteration = 100000
    chosenPairs = []
    for i in range(iteration):
      pairs = self.pair.generateWeighted(self.weightedMatrix)
      #choose the first one of these pairs (Strategy Mono)
      pair = pairs[0]
      #turn pair into str to make a dictionary from
      chosenPairs.append(str(pair))
    #generate frequency dictionary
    frequency = dict(collections.Counter(chosenPairs))
    #check for all weight pairs if the weight corresponds to the iteration amount divided by the frequency
    for indexString, weight in weightPairs:
      stohasticFrequency = (frequency[indexString] / iteration) * totalWeight
      print(f"Checking between {weight} and {stohasticFrequency}")
      self.assertEqual(weight, round(stohasticFrequency))





