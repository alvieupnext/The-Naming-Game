from matplotlib import pyplot as plt
from variants.ABNG import *
from namingGameTools import Strategy, MatrixFactory as mf
import numpy as np
from pylab import plot, show, \
                  legend, violinplot, setp

numberOfAgents = 100

consensusScoreList = [0.8, 0.9,0.95, 0.98, 0.99, 1]

ng = ABNG(maxIterations=2000, simulations=100, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=consensusScoreList, display=False)

maxNeighbourSize = 40

#test every single neighbourhood size from 2 to maximum
neighboursizes = list(range(5, maxNeighbourSize + 1, 5))

plt.title(f"Consensus Time Per Neighbourhood Size({ng.name}, {ng.strategy.__name__}, {ng.simulations} simulations, {numberOfAgents} agents)")

plt.ylabel("Amount of Games played")

plt.xlabel("Neighbour Size of Agent")

colors = ['blue', 'red', 'cyan', 'magenta', 'green', 'purple']

#help procedures for the boxplot
# function for setting the colors of the box plots pairs
def setBoxColors(bp):
  for index, box in enumerate(bp['bodies']):
    setp(box, color=colors[index])




consensusIterations = []

#create an empty matrix (rows are consensusScores, columns are number of neighbours)
consensusMatrix = np.zeros((len(neighboursizes), len(consensusScoreList)), dtype=object)

positions = [[n for n in range(i, i + len(consensusScoreList))] for i in range(0, len(neighboursizes) * len(consensusScoreList), len(consensusScoreList))]

print(positions)

ticks = [np.mean(lst) for lst in positions]
print(ticks)
# ax.set_xticks(ticks)

for row, neighbour in enumerate(neighboursizes):
  print(f"Using Neighbour Size {neighbour}")
  lattice = mf.MatrixFactory().makeLatticeMatrix(numberOfAgents, neighbour)
  output = ng.start(lattice)
  #get list of when consensus was reached for every simulation
  consensusList = output["consensus"]
  reformattedConsensusList = []
  for value in consensusScoreList:
    reformattedConsensusList.append([])
  for simulationConsensus in consensusList:
    for index, set in enumerate(simulationConsensus):
      #get the right iteration from consensusList and append it to the reformatted list
      reformattedConsensusList[index].append(set[1])
  print(reformattedConsensusList)
  for column, values in enumerate(reformattedConsensusList):
    consensusMatrix[row, column] = values

lines = [plot([1,1], color = color)[0] for color in colors]

consensusScoreStringList = [f"Convergence Rate : {rate}" for rate in consensusScoreList]

legend(lines,consensusScoreStringList)

list(map(lambda handle: handle.set_visible(False), lines))

for index, row in enumerate(consensusMatrix):
  vp = violinplot(row, positions=positions[index], widths=0.6)
  setBoxColors(vp)

plt.xticks(ticks, neighboursizes)

show()

