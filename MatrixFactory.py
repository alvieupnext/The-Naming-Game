import numpy as np
import random as r

def generate1(frm, to):
  return 1

class MatrixFactory:
  #sym indicates whether the output adjacency matrix is symmetrical or not (default False)
  #type indicates the type of the matrix elements (default int)
  #order indicates the indexing order (default columns)
  #generateWeight creates a weight for a connection (by default returns 1)
  def __init__(self, triangular = True, type = float, order ='C', random = None, generateWeight = generate1):
    self.triangular = triangular
    self.type = type
    self.order = order
    self.random = random
    self.generateWeight = generateWeight

  #create an empty square matrix
  def __createSquareMatrix(self, dim):
    matrixDimensions = (dim, dim)
    # create a new matrix filled with zeroes
    # order can be interesting for future calculations
    return np.zeros(matrixDimensions, dtype=self.type, order=self.order)

  #create a new lattice
  def makeLatticeMatrix(self, numberOfAgents, numberOfNeighbors):
    #create matrix
    lattice = self.__createSquareMatrix(numberOfAgents)

    #generate symmetrical neighbors connection for the first agent (agent 0 at column 0)
    # scanNeighbours could be refactored to better match the usage of the variable
    # has to be even
    # generate neighbors for agent 1
    # scanNeighbours could be refactored to better match the usage of the variable
    scanNeighbours = numberOfNeighbors // 2
    for neighbourTeller in range(scanNeighbours):
      # neighbourTeller gets incremented because Python range works from [0, scanNeighbours[, incrementing will exclude 0 and include scanNeighbours
      # MATLAB chooses first the column and then the row as opposed to numPy where matrices are represented as array of arrays, where an array represents a row, therefore
      # the row has to be chosen first
      lattice[1 + neighbourTeller, 0] = 1
      lattice[numberOfAgents - (neighbourTeller + 1), 0] = 1

    # generate neighbors for the other agents using circular shifting
    # we have to shift the row one position to the right
    # and wrap around cells that shift outside of the matrix
    for shiftTeller in range(1, numberOfAgents):
      lattice[:, shiftTeller] = np.roll(lattice[:, shiftTeller - 1], 1)

    # turn lattice matrix triangular (if matrices are symmetrical) (lower triangular matrix)
    # because otherwise every link between two agents is represented by two 1's
    # for instance agent 5 and 3 are connected
    # => element (3,5) and (5,3) of the latticeMatrix are 1
    #
    if self.triangular:
      lattice = np.tril(lattice)

    #right now all values are one, update all values to reflect generateWeight
    nonZero = np.nonzero(lattice)
    nonZeroIdx = np.transpose(nonZero)

    if self.triangular:
      for row, column in nonZeroIdx:
        weight = self.generateWeight(row, column)
        lattice[row, column] = weight

    return lattice

  #TODO try to fix scaleFree with numberOfEstablishedLinks
  #create a new scale free matrix
  def makeScaleFreeMatrix(self, numberOfAgents, numberOfEstablishedLinks = 2):
    # create matrix
    scaleFree = self.__createSquareMatrix(numberOfAgents)

    # define the starting connections
    scaleFree[1, 0] = self.generateWeight(1, 0)
    scaleFree[3, 0] = self.generateWeight(3, 0)
    scaleFree[2, 1] = self.generateWeight(2, 1)
    scaleFree[3, 2] = self.generateWeight(3, 2)

    # if matrix output isn't triangular, add the double connections to indicate two-way connection
    if not self.triangular:
      scaleFree[0,1] = scaleFree[1, 0]
      scaleFree[0,3] = scaleFree[3, 0]
      scaleFree[1,2] = scaleFree[2, 1]
      scaleFree[2,3] = scaleFree[3, 2]

    #to control the randomness of the output, set seed here
    r.seed(self.random)

    # now we need to select a random node, but the chance to select node n has
    # to be proportional to the number of connections already ending in node n
    # we can achieve this by selecting a random non-zero value in the connection
    # matrix, and looking up the row number

    for newNode in range(4, numberOfAgents):
      establishedLinks = 0;
      # find non zero elements
      rows, columns = np.nonzero(scaleFree)
      while establishedLinks < numberOfEstablishedLinks:
        # get amount of non zero elements
        amount = len(rows)
        # amount has to be decremented because randint considers both bounds aswell
        #set seed
        # generate a random number to choose edge
        chosenEdge = r.randint(0, amount - 1)
        # get the node from the rows array
        chosenNode = rows[chosenEdge]
        # if there isn't a connection prior, establish one
        if scaleFree[chosenNode, newNode] == 0 and scaleFree[newNode, chosenNode] == 0:
          weight = 0
          if chosenNode > newNode:
            weight = self.generateWeight(chosenNode, newNode)
          else:
            weight = self.generateWeight(newNode, chosenNode)
          #if the matrix isn't triangular, add both connections
          if not self.triangular:
            scaleFree[chosenNode, newNode] = weight
            scaleFree[newNode, chosenNode] = weight
          #if symmetrical, only add the connection under the main diagonal
          else:
            # Property: in a lower triangular matrix, the row number has to always be higher than the column number
            if chosenNode > newNode:
              scaleFree[chosenNode, newNode] = weight
            else:
              scaleFree[newNode, chosenNode] = weight
          # increase established links
          establishedLinks += 1

    return scaleFree

  #create a new small world matrix
  def makeSmallWorldMatrix(self, numberOfAgents, numberOfNeighbors, numberOfRandomLinks = 3):
    #first step is creating a new lattice
    smallWorld = self.makeLatticeMatrix(numberOfAgents, numberOfNeighbors)
    # then we generate random connections
    amount = 0
    r.seed(self.random)
    while amount < numberOfRandomLinks:
      # get two random agents
      x = r.randint(0, numberOfAgents - 1);
      y = r.randint(0, numberOfAgents - 1);
      # make sure they are not equal to each other
      # if they have no prior connection, create the connection
      if (not x == y) and smallWorld[x, y] == 0 and smallWorld[y, x] == 0:
        weight = 0
        if x > y:
          weight = self.generateWeight(x, y)
        else:
          weight = self.generateWeight(y, x)
        #if matrix isn't triangular, we need to two-way connect
        if not self.triangular:
          smallWorld[x, y] = weight
          smallWorld[y, x] = weight
        #if symmetrical, just fill in the information for a lower triangular matrix
        elif x > y:
          smallWorld[x, y] = weight
        else:
          smallWorld[y, x] = weight
        amount += 1
    return smallWorld

  def generateSmallWorldPopulation(self, population, numberOfAgents, maxRandom = 10):
    #establish max amount of connections an agent can have
    maxConnections = (numberOfAgents - 1) // 2
    generatedPopulation = []
    for _ in range(population):
      #get a random number of neighbors
      noNeighbors = maxConnections
      #get a random number of random connections
      noRandom = r.randint(0, maxRandom)
      #calculate the overflow in connections
      overflow = noNeighbors + noRandom - maxConnections
      if overflow > 0:
        #remove overflow from the number of neighbors
        noNeighbors -= overflow
      generatedPopulation.append(self.makeSmallWorldMatrix(numberOfAgents, noNeighbors, noRandom))
    return generatedPopulation














