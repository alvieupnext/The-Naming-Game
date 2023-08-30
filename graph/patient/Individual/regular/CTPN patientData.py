from matplotlib import pyplot as plt
from variants.ABNG import *
from namingGameTools import Strategy
from patients.patientData import *
import numpy as np

numberOfAgents = brumeg_functional_agents

consensusScoreList = [0.8, 0.9,0.95, 0.98, 0.99, 1]

ng = ABNG(maxIterations=1000, simulations=1, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=consensusScoreList, display=False)

patient_data = brumeg_functional

#Get the patient names from the Subject column
patientNames = patient_data['Subject'].tolist()

# For only choosing a subset of patients
patientNames = patientNames[0:1]

# groupSize = len(patientNames) // 4
groupSize = 1

print(groupSize)


patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

colors = ['blue', 'red', 'cyan', 'magenta', 'green', 'purple']

#help procedures for the boxplot
# function for setting the colors of the box plots pairs
def setBoxColors(bp):
  for index, box in enumerate(bp['boxes']):
    plt.setp(box, color=colors[index])

for i, patientGroup in enumerate(patientGroups):
  plt.title(
    f"Consensus Time Per Patient({ng.name}, {ng.simulations} simulations, using patient SC group {i} with size {groupSize})")

  plt.ylabel("Amount of Games played")

  plt.xlabel("Patient Number")
  # create an empty matrix (rows are consensusScores, columns are the patients)
  consensusMatrix = np.zeros((len(patientGroup), len(consensusScoreList)), dtype=object)

  positions = [[n for n in range(i, i + len(consensusScoreList))] for i in
               range(0, len(patientGroup) * len(consensusScoreList), len(consensusScoreList))]

  ticks = [np.mean(lst) for lst in positions]

  for row, patient in enumerate(patientGroup):
    print(f"Using Patient Data {patient}")
    #Get the patient data from the pandas
    data = readFromPandasDataframe(patient_data, patient)
    matrix = convertArrayToMatrix(data, numberOfAgents)
    output = ng.start(matrix)
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
    #fill a row of the consensusMatrix
    for column, values in enumerate(reformattedConsensusList):
      consensusMatrix[row, column] = values

  lines = [plt.plot([1, 1], color=color)[0] for color in colors]

  consensusScoreStringList = [f"Convergence Rate : {rate}" for rate in consensusScoreList]

  plt.legend(lines, consensusScoreStringList)

  list(map(lambda handle: handle.set_visible(False), lines))

  for index, row in enumerate(consensusMatrix):
    bp = plt.boxplot(row, positions=positions[index], widths=0.6)
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

  plt.show()




