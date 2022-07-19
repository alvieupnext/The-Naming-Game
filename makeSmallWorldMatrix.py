import random as r
import makeLatticeMatrix as lattice

# Implementation of the MATLAB code written for the Multi Agent Learning Project by Guy Nagels

#NOTE: Python, like most general-use languages, starts arrays at index 0 while MATLAB starts arrays at index 1

#This functions takes a number of agents and a number of neighbors and returns a lattice matrix
def makeSmallWorldMatrix(numberOfAgents, numberOfNeighbors, numberOfRandomLinks):

  #create a lattice matrix
  latticeA = lattice.makeLatticeMatrix(numberOfAgents, numberOfNeighbors)

  #generate random connections
  amount = 0
  while amount<numberOfRandomLinks:
    #get two random agents
      x = r.randint(0, numberOfAgents-1);
      y = r.randint(0, numberOfAgents-1);
    #make sure they are not equal to each other
    # ???? why <
      if not x == y and latticeA[x, y] != 1:
        #if they have no prior connection, create the connection
        latticeA[x, y] = 1
        latticeA[y, x] = 1
        amount += 1

  return latticeA



print(makeSmallWorldMatrix(20,4,5))