import numpy as np
import random as r
class AgentPairs:
  def __init__(self):

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

