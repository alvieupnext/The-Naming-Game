import numpy as np

# Implementation of the MATLAB code written for the Multi Agent Learning Project by Guy Nagels

#NOTE: Python, like most general-use languages, starts arrays at index 0 while MATLAB starts arrays at index 1

#This functions takes a number of agents and a number of neighbors and returns a lattice matrix
def makeLatticeMatrix(numberOfAgents, numberOfNeighbors):
  #define the dimensions of the matrix
  latticeDimensions = (numberOfAgents, numberOfAgents)

  #create a new matrix filled with zeroes
  #order can be interesting for future calculations
  latticeA = np.zeros(latticeDimensions, dtype=int, order='C')

  #generate neighbors for agent 1
  #scanNeighbours could be refactored to better match the usage of the variable
  scanNeighbours = numberOfNeighbors // 2
  for neighbourTeller in range(scanNeighbours):
    #neighbourTeller gets incremented because Python range works from [0, scanNeighbours[, incrementing will exclude 0 and include scanNeighbours
    #MATLAB chooses first the column and then the row as opposed to numPy where matrices are represented as array of arrays, where an array represents a row, therefore
    #the row has to be chosen first
    latticeA[1+neighbourTeller, 0] = 1
    latticeA[numberOfAgents-(neighbourTeller+1), 0] = 1

  #generate neighbors for the other agents using circular shifting
  #we have to shift the row one position to the right
  #and wrap around cells that shift outside of the matrix
  for shiftTeller in range(1, numberOfAgents):
    latticeA[:, shiftTeller] = np.roll(latticeA[:, shiftTeller-1], 1)

  #turn lattice matrix triangular
  #because otherwise every link between two agents is represented by two 1's
  #for instance agent 5 and 3 are connected
  #=> element (3,5) and (5,3) of the latticeMatrix are 1

 # latticeA = np.tril(latticeA)

  return latticeA



# print(makeLatticeMatrix(20,5))