import numpy as np
import random as r

def pairAgentsVillatoroWise(networkMatrix):

  numberOfPairs = len(networkMatrix)//2
  agentPairs = np.zeros((numberOfPairs, 2))

  #it suffices to perform this selection once
  rows, columns = np.nonzero(networkMatrix)
  amount = len(rows)

  for i in range(numberOfPairs):
   # rows, columns = np.nonzero(networkMatrix) MATLAB PLACEMENT (INEFFICIENT)
    # randomly select one of these connected pairs of agents
    # if amount>0: INEFFICIENT AMOUNT TESTS
    # get one of the edges at random
    selection = r.randint(0, amount - 1)
    # get one agent associated with the connection
    chosenColumn = columns[selection]
    # assign an agent with this associated agent
    agentPairs[i, 0] = i
    agentPairs[i, 1] = chosenColumn
  return agentPairs