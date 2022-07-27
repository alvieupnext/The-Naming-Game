from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
from variants.ABNG import *
import MatrixFactory as mf
import Strategy
import numpy as np

ng = ABNG(maxIterations=1000, simulations=5, strategy=Strategy.multi, output=["popularity", "consensus"], consensusScore=1, display=False)

numberOfAgents = 200

maxNeighbourSize = 20

plt.title(f"Consensus Time Per Neighbourhood Size({ng.name}, {ng.strategy.__name__}, {numberOfAgents} agents)")

plt.ylabel("Amount of Games played")

plt.xlabel("Neighbour Size of Agent")

#test every single neighbourhood size from 2 to maximum
neighboursizes = list(range(2, maxNeighbourSize + 1, 2))

consensusIterations = []

for neighbour in neighboursizes:
  lattice = mf.MatrixFactory().makeLatticeMatrix(numberOfAgents, neighbour)
  output = ng.start(lattice)
  #get list of when consensus was reached for every simulation
  consensusList = output["consensus"]
  mean = np.mean(consensusList)
  #add this mean value to consensusIterations
  consensusIterations.append(mean)

plt.plot(neighboursizes, consensusIterations)

plt.show()


