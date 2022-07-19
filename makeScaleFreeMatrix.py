import numpy as np
import random as r

# Implementation of the MATLAB code written for the Multi Agent Learning Project by Guy Nagels

#NOTE: Python, like most general-use languages, starts arrays at index 0 while MATLAB starts arrays at index 1

#This functions takes a number of agents and a number of neighbors and returns a scale free matrix, free to be expanded in neighbors
def makeScaleFreeMatrix(numberOfAgents):
  # define the dimensions of the matrix
  latticeDimensions = (numberOfAgents, numberOfAgents)

  #NOTE: why latticeA name
  # create a new matrix filled with zeroes
  # order can be interesting for future calculations
  latticeA = np.zeros(latticeDimensions, dtype=int, order='C')

  #indices have to be subtracted by 1 compared to MATLAB
  latticeA[1,0] = 1
  latticeA[0,1] = 1
  latticeA[3,0] = 1
  latticeA[0,3] = 1
  latticeA[2,1] = 1
  latticeA[1,2] = 1
  latticeA[2,3] = 1
  latticeA[3,2] = 1

  # now we need to select a random node, but the chance to select node n has
  # to be proportional to the number of connections already ending in node n
  # we can achieve this by selecting a random non-zero value in the connection
  #matrix, and looking up the row number

  for newNode in range(4, numberOfAgents):
    establishedLinks = 0;
    #find non zero elements
    rows, columns = np.nonzero(latticeA)
    while establishedLinks < 2:
      #get amount of non zero elements
      amount = len(rows)
      #amount has to be decremented because randint considers both bounds aswell
      #generate a random number to choose edge
      chosenEdge = r.randint(0, amount - 1)
      #get the node from the rows array
      chosenNode = rows[chosenEdge]
      #if there isn't a connection prior, establish one
      if latticeA[chosenNode, newNode] == 0:
        latticeA[chosenNode, newNode] = 1
        latticeA[newNode, chosenNode] = 1
        #increase established links
        establishedLinks += 1

      #just as makeLatticeMatrix, we can make the matrix triangular
      #latticeA = np.tril(latticeA)


  return latticeA

print(makeScaleFreeMatrix(20))

