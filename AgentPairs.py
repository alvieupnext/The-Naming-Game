import numpy as np
import random as r
class AgentPairs:
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
  def generate(self, networkMatrix):
    numberOfPairs = len(networkMatrix)//2
    #start agent pairs as empty
    agentPairs = []
    #get rownumbers and columnnumbers from non zero elements
    rowNrs, columnNrs = np.nonzero(networkMatrix)

    for i in range(numberOfPairs):
      #get amount of non zero elements
      amount = len(rowNrs)
      # randomly select one of these connected pairs of agents
      if amount>0:
        #get one of the edges at random
        selection = r.randint(0, amount - 1)
        #get both agents associated with the connection
        chosenRow = rowNrs[selection]
        chosenColumn = columnNrs[selection]
        #assign them as pair
        newPair = [chosenRow, chosenColumn] #could be a set
        agentPairs.append(newPair)
        #make sure these agents can't return by removing every combination involving either one of the agents from row and column
        filterRow = []
        filterColumn = []
        #this code could be compressed into one pass (but this is more readable in my opinion)
        for rowNr in rowNrs:
          #only consider column if the matrix isn't symmetrical (could be improved)
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

  #Weighted method
  def generateWeighted(self, networkMatrix):
    numberOfPairs = len(networkMatrix)//2
    # start agent pairs as empty
    agentPairs = []
    #get non zero indices from network
    nonZero = np.nonzero(networkMatrix)
    #get non zero row column pair
    #transpose will return an array with as elements an array of a row and column
    nonZeroIdx = np.transpose(nonZero)
    for i in range(numberOfPairs):
      # get non zero values
      nonZeroValues = networkMatrix[nonZero]
      #get amount of non zero elements
      amount = len(nonZeroValues)
      #if we still have non zero values
      if amount > 0:
        #make a random choice (weighted using the values)
        print(f"nonZeroIDX is {nonZeroIdx}")
        print(nonZeroValues)
        chosenIdx, = r.choices(nonZeroIdx, weights=nonZeroValues)
        #add chosen IDX to agent pairs
        agentPairs.append(chosenIdx)
        #update nonZeroIDX to remove the chosen agents
        chosenRow = chosenIdx[0]
        chosenCol = chosenIdx[1]
        nonZeroIdx = list(filter(lambda pair: not (chosenRow in pair or chosenCol in pair), nonZeroIdx))
        print(f"nonZeroIDX became {nonZeroIdx}")
        # update nonZero
        nonZero = ([], [])
        for pair in nonZeroIdx:
          nonZero[0].append(pair[0])
          nonZero[1].append(pair[1])
    return agentPairs



