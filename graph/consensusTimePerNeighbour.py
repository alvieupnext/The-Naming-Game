from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
from variants.ABNG import *
import MatrixFactory as mf
import Strategy
import numpy as np
from pylab import plot, show, savefig, xlim, figure, \
                  ylim, legend, boxplot, setp, axes

#TODO clean this code
numberOfAgents = 100

consensusScoreList = [0.8, 0.9,0.95, 0.98, 0.99, 1]

ng = ABNG(maxIterations=2000, simulations=100, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=consensusScoreList, display=False)

maxNeighbourSize = 40

#test every single neighbourhood size from 2 to maximum
neighboursizes = list(range(5, maxNeighbourSize + 1, 5))

fig = figure()
ax = axes()

plt.title(f"Consensus Time Per Neighbourhood Size({ng.name}, {ng.strategy.__name__}, {ng.simulations} simulations, {numberOfAgents} agents)")

plt.ylabel("Amount of Games played")

plt.xlabel("Neighbour Size of Agent")



#help procedures for the boxplot
# function for setting the colors of the box plots pairs
def setBoxColors(bp):
  #color for 0.8
    setp(bp['boxes'][0], color='blue')
  # color for 0.9
    setp(bp['boxes'][1], color='red')
  # color for 0.95
    setp(bp['boxes'][2], color='cyan')
  # color for 0.98
    setp(bp['boxes'][3], color='magenta')
 # color for 0.99
    setp(bp['boxes'][4], color='green')
  # color for 1
    setp(bp['boxes'][5], color='purple')



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
  print(consensusList)
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

print(consensusMatrix)

hB, = plot([1,1],'b-')
hR, = plot([1,1],'r-')
hC, = plot([1,1], 'c-')
hM, = plot([1,1], 'm-')
hG, = plot([1,1], 'g-')
hP, = plot([1,1], color='purple')

legend((hB, hR, hC, hM, hG,hP),('Convergence Rate: 0.8', 'Convergence Rate: 0.9', 'Convergence Rate: 0.95', "Convergence Rate: 0.98", "Convergence Rate: 0.99", 'Convergence Rate: 1'))
hB.set_visible(False)
hR.set_visible(False)
hC.set_visible(False)
hM.set_visible(False)
hG.set_visible(False)
hP.set_visible(False)



for index, row in enumerate(consensusMatrix):
  bp = boxplot(row, positions=positions[index], widths=0.6)
  setBoxColors(bp)

plt.xticks(ticks, neighboursizes)

show()

