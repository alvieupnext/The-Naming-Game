import numpy as np
import random as r
class AgentPairs:
  def __init__(self):
    pass

  #Villatoro wise
  def generateVillatoro(self, networkMatrix):
    numberOfPairs = len(networkMatrix) // 2
    agentPairs = np.zeros((numberOfPairs, 2))

    # it suffices to perform this selection once
    rows, columns = np.nonzero(networkMatrix)
    amount = len(rows)

    for i in range(numberOfPairs):
      # randomly select one of these connected pairs of agents
      # get one of the edges at random
      selection = r.randint(0, amount - 1)
      # get one agent associated with the connection
      chosenColumn = columns[selection]
      # assign an agent with this associated agent
      agentPairs[i, 0] = i
      agentPairs[i, 1] = chosenColumn
    return agentPairs

  #Our method
  def generate(self, networkMatrix, symmetrical=False):
    numberOfPairs = len(networkMatrix)//2
    #start agent pairs as empty
    agentPairs = []
    #get rownumbers and columnnumbers from non zero elements
    rowNrs, columnNrs = np.nonzero(networkMatrix)

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
        #this code could be compressed into one pass (but this is more readable in my opinion)
        for rowNr in rowNrs:
          #only consider column if the matrix isn't symmetrical
          filterRow.append(chosenRow == rowNr or chosenColumn == rowNr)
        for columnNr in columnNrs:
          #only consider row if the matrix isn't symmetrical
          filterColumn.append(chosenColumn == columnNr or chosenRow == columnNr)
        #merge both filter arrays to create the final filter array
        #inverting row or column as we are interested in the elements that don't contain either a chosen row or column
        filterArray = [not (row or column) for row, column in zip(filterRow, filterColumn)]
        #update both arrays by filtering the used agents
        rowNrs = rowNrs[filterArray]
        columnNrs = columnNrs[filterArray]
    return agentPairs

