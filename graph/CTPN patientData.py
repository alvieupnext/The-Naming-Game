from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
from variants.ABNG import *
import MatrixFactory as mf
import Strategy
import numpy as np
from pylab import plot, show, \
                  legend, boxplot, setp
from readPatientData import *

numberOfAgents = 100

consensusScoreList = [0.8, 0.9,0.95, 0.98, 0.99, 1]

ng = ABNG(maxIterations=2000, simulations=100, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=consensusScoreList, display=False)

patientNames = names

groupSize = len(patientNames) // 5


patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

print(patientGroups)

colors = ['blue', 'red', 'cyan', 'magenta', 'green', 'purple']

#help procedures for the boxplot
# function for setting the colors of the box plots pairs
def setBoxColors(bp):
  for index, box in enumerate(bp['boxes']):
    setp(box, color=colors[index])

for i, patientGroup in enumerate(patientGroups):
  plt.title(
    f"Consensus Time Per Patient({ng.name}, {ng.simulations} simulations, using patient SC group {i} with size {groupSize})")

  plt.ylabel("Amount of Games played")

  plt.xlabel("Patient Number")
  # create an empty matrix (rows are consensusScores, columns are number of neighbours)
  consensusMatrix = np.zeros((len(patientGroup), len(consensusScoreList)), dtype=object)

  positions = [[n for n in range(i, i + len(consensusScoreList))] for i in
               range(0, len(patientGroup) * len(consensusScoreList), len(consensusScoreList))]

  ticks = [np.mean(lst) for lst in positions]

  for row, patient in enumerate(patientGroup):
    print(f"Using Patient Data {patient}")
    data = readPatientData(patient, 40)
    output = ng.start(data)
    #get list of when consensus was reached for every simulation
    consensusList = output["consensus"]
    # reformat list to get the iteration values
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

  lines = [plot([1, 1], color=color)[0] for color in colors]

  consensusScoreStringList = [f"Convergence Rate : {rate}" for rate in consensusScoreList]

  legend(lines, consensusScoreStringList)

  list(map(lambda handle: handle.set_visible(False), lines))

  for index, row in enumerate(consensusMatrix):
    bp = boxplot(row, positions=positions[index], widths=0.6)
    setBoxColors(bp)
    # for position, simValues in zip(positions[index], row):
    #   # generate a linear space from 0 to 1 to scatter points
    #   clevels = np.linspace(0., 1., len(simValues))
    #   # generate positionList
    #   positionList = [position - 0.5 + clevels[i] for i in range(len(simValues))]
    #   print(positionList)
    #   print(simValues)
    #   plt.scatter(positionList, simValues, alpha=0.4)

  plt.xticks(ticks, patientGroup)

  show()




