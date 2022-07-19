import numpy as np
import random as r

class MatrixFactory:
  #sym indicates whether the output adjacency matrix is symmetrical or not (default False)
  #type indicates the type of the matrix elements (default int)
  #order indicates the indexing order (default columns
  def __init__(self, sym = True, type = int, order = 'C'):
    self.sym = sym
    self.type = type
    self.order = order

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

    #generate neighbors connection for the first agent (agent 0 at column 0)
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

    # turn lattice matrix triangular (if matrices are symmetrical) (under triangular matrix)
    # because otherwise every link between two agents is represented by two 1's
    # for instance agent 5 and 3 are connected
    # => element (3,5) and (5,3) of the latticeMatrix are 1
    #
    if self.sym:
      return np.tril(lattice)
    else: return lattice

  #create a new scale free matrix
  def makeScaleFreeMatrix(self, numberOfAgents):
    # create matrix
    scaleFree = self.__createSquareMatrix(numberOfAgents)

    # define the starting connections
    scaleFree[1, 0] = 1
    scaleFree[3, 0] = 1
    scaleFree[2, 1] = 1
    scaleFree[3, 2] = 1

    # if matrix factory isn't symmetrical, add the double connections to indicate two-way connection
    if not self.sym:
      scaleFree[0,1] = 1
      scaleFree[0,3] = 1
      scaleFree[1,2] = 1
      scaleFree[2,3] = 1

    # now we need to select a random node, but the chance to select node n has
    # to be proportional to the number of connections already ending in node n
    # we can achieve this by selecting a random non-zero value in the connection
    # matrix, and looking up the row number

    for newNode in range(4, numberOfAgents):
      establishedLinks = 0;
      # find non zero elements
      rows, columns = np.nonzero(scaleFree)
      while establishedLinks < 2:
        # get amount of non zero elements
        amount = len(rows)
        # amount has to be decremented because randint considers both bounds aswell
        # generate a random number to choose edge
        chosenEdge = r.randint(0, amount - 1)
        # get the node from the rows array
        chosenNode = rows[chosenEdge]
        # if there isn't a connection prior, establish one
        if scaleFree[chosenNode, newNode] == 0:
          #if the matrix isn't symmetrical, add both connections
          if not self.sym:
            scaleFree[chosenNode, newNode] = 1
            scaleFree[newNode, chosenNode] = 1
          #if symmetrical, only add the connection under the main diagonal
          else:
            # Property: in a lower triangular matrix, the row number has to always be higher than the column number
            if chosenNode > newNode:
              scaleFree[chosenNode, newNode] = 1
            else:
              scaleFree[newNode, chosenNode] = 1
          # increase established links
          establishedLinks += 1

    return scaleFree







