import numpy as np
import random as r

def pairAgents(networkMatrix):

  numberOfPairs = len(networkMatrix)//2
  agentPairs = np.zeros((numberOfPairs, 2))

  for i in range(numberOfPairs):
    #get rownumbers and columnnumbers from non zero elements
    rowNrs, columnNrs = np.nonzero(networkMatrix) #could be improved
    amount = len(rowNrs)
    # randomly select one of these connected pairs of agents
    if amount>0:
      #get one of the edges at random
      selection = r.randint(0, amount - 1)
      #get both agents associated with the connection
      chosenRow = rowNrs[selection]
      chosenColumn = columnNrs[selection]
      #assign them as pair
      agentPairs[i, 0] = chosenRow
      agentPairs[i, 1] = chosenColumn
      #make sure these agents can't return by making the row and column for both agents 0
      networkMatrix[chosenColumn, :] = 0
      networkMatrix[chosenRow, :] = 0
      networkMatrix[:, chosenColumn] = 0
      networkMatrix[:, chosenRow] = 0

  return agentPairs