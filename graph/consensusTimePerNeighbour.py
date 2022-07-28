from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
from variants.ABNG import *
import MatrixFactory as mf
import Strategy
import numpy as np

numberOfAgents = 100

consensusScoreList = [0.7, 0.8, 0.85, 0.9, 0.95, 1]

ng = ABNG(maxIterations=1000, simulations=5, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=consensusScoreList, display=False)

maxNeighbourSize = 40

#test every single neighbourhood size from 2 to maximum
neighboursizes = list(range(2, maxNeighbourSize + 1, 2))

plt.title(f"Consensus Time Per Neighbourhood Size({ng.name}, {ng.strategy.__name__}, {numberOfAgents} agents)")

plt.ylabel("Amount of Games played")

plt.xlabel("Neighbour Size of Agent")



consensusIterations = []

#create an empty matrix (rows are consensusScores, columns are number of neighbours)
consensusMatrix = np.zeros((len(consensusScoreList), len(neighboursizes)))

for neighbour in neighboursizes:
  print(f"Using Neighbour Size {neighbour}")
  lattice = mf.MatrixFactory().makeLatticeMatrix(numberOfAgents, neighbour)
  output = ng.start(lattice)
  #get list of when consensus was reached for every simulation
  consensusList = output["consensus"]
  print(consensusList)
  reformattedConsensusList = []
  for value in consensusScoreList:
    reformattedConsensusList.append((value, []))
  for simulationConsensus in consensusList:
    for index, set in enumerate(simulationConsensus):
      #get the right iteration from consensusList and append it to the reformatted list
      reformattedConsensusList[index][1].append(set[1])
  print(reformattedConsensusList)
  mean = np.mean(consensusList)
  #add this mean value to consensusIterations
  consensusIterations.append(mean)

plt.plot(neighboursizes, consensusIterations)

plt.show()


