from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
from variants.ABNG import *
import MatrixFactory as mf
import Strategy
import numpy as np
from pylab import plot, show, \
                  legend, boxplot, setp

numberOfAgents = 100

consensusScoreList = [0.6, 0.65, 0.69, 0.7]

ng = ABNG(maxIterations=10000, simulations=10, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=consensusScoreList, display=False)

#test every single establishing links from 1 to 3
establishingLinks = list(range(1, 4))

plt.title(f"Consensus Time Per Establishing Link Size({ng.name}, {ng.strategy.__name__}, {ng.simulations} simulations, {numberOfAgents} agents)")

plt.ylabel("Amount of Games played")

plt.xlabel("Neighbour Size of Agent")

colors = ['blue', 'red', 'cyan', 'magenta', 'green', 'purple']

#help procedures for the boxplot
# function for setting the colors of the box plots pairs
def setBoxColors(bp):
  for index, box in enumerate(bp['boxes']):
    setp(box, color=colors[index])

consensusIterations = []

#create an empty matrix (rows are consensusScores, columns are number of neighbours)
consensusMatrix = np.zeros((len(establishingLinks), len(consensusScoreList)), dtype=object)

positions = [[n for n in range(i, i + len(consensusScoreList))] for i in range(0, len(establishingLinks) * len(consensusScoreList), len(consensusScoreList))]

print(positions)

ticks = [np.mean(lst) for lst in positions]
print(ticks)

for row, link in enumerate(establishingLinks):
  print(f"Using Establishing Link Size {link}")
  scaleFree = mf.MatrixFactory().makeScaleFreeMatrix(numberOfAgents, link)
  output = ng.start(scaleFree)
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
  bp = boxplot(row, positions=positions[index], widths=0.6)
  setBoxColors(bp)
  # #code for scatterplotting
  # ngroup = len(row)
  # clevels = np.linspace(0., 1., ngroup)
  # for position, simValues in zip(positions[index], row):
  #   positionList = [position] * len(simValues)
  #   print(positionList)
  #   print(simValues)
  #   plt.scatter(positionList, simValues, alpha=0.4)




plt.xticks(ticks, establishingLinks)

show()

