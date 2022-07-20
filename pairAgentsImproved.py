import numpy as np
import makeLatticeMatrix as lattice
import random as r

#this version of pair Agents is used in AgentPairs
#first improvement, making array dynamic to amount of actual pairs (return value is no longer a numpy array of arrays) (use np.array for that)
#second improvement, get non-zero elements once from matrix and update this list after choosing agents instead of recalculating
def pairAgentsImproved(networkMatrix, symmetrical=True):

  numberOfPairs = len(networkMatrix)//2
  #start agent pairs as empty
  agentPairs = []
  #get rownumbers and columnnumbers from non zero elements
  rowNrs, columnNrs = np.nonzero(networkMatrix)
  amount = len(rowNrs)


  for i in range(numberOfPairs):
    #get rownumbers and columnnumbers from non zero elements
    amount = len(rowNrs)
    # randomly select one of these connected pairs of agents
    if amount>0:
      #get one of the edges at random
      selection = r.randint(0, amount - 1)
      #get both agents associated with the connection
      chosenRow = rowNrs[selection]
      chosenColumn = columnNrs[selection]
      #assign them as pair
      newPair = [chosenRow, chosenColumn]
      agentPairs.append(newPair)
      #make sure these agents can't return by removing every combination involving either one of the agents from row and column
      filterRow = []
      filterColumn = []
      ##if symmetrical is true, we only have to remove row -> x and x -> column combinations
      ##if symmetrical is false, we have to consider also column -> x and x -> row combinations
      for rowNr in rowNrs:
        #only consider column if the matrix isn't symmetrical
        filterRow.append(chosenRow == rowNr or (not symmetrical and chosenColumn == rowNr))
      for columnNr in columnNrs:
        #only consider row if the matrix isn't symmetrical
        filterColumn.append(chosenColumn == columnNr or (not symmetrical and chosenRow == columnNr))
      #merge both filter arrays to create the final filter array
      #inverting row or column as we are interested in the elements that don't contain either a chosen row or column
      filterArray = [not (row or column) for row, column in zip(filterRow, filterColumn)]
      #update both arrays by filtering the used agents
      rowNrs = rowNrs[filterArray]
      columnNrs = columnNrs[filterArray]





  return agentPairs


array = pairAgentsImproved(lattice.makeLatticeMatrix(20,4))

print(array)
print(len(array))