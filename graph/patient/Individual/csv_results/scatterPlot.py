from matplotlib import pyplot as plt
from patients.patientData import *

patientData = brumeg_functional_convergence

patientNames = patientData['Subject'].unique().tolist()

# groupSize = len(patientNames) // 20
groupSize = 5

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

chosenConvergence = 0.95

print(patientGroups)

def scatterPlot():
  for i, patientGroup in enumerate(patientGroups[3:]):
    plt.title(f"Scatter Plot Convergence with {chosenConvergence} with patient group {i}")
    plt.ylabel("Amount of Games played")
    plt.xlabel("Patient Number")
    convergencePoints = []
    for index, patient in enumerate(patientGroup):
      consensusList = getConsensusIterationOfSubject(patientData, patient, chosenConvergence)
      # make a list of all positions (all to be scattered around the index)
      # generate a linear space from 0 to 1 to scatter points
      linspace = np.linspace(0., 1., len(consensusList))
      positionList = [index - 0.5 + linspace[i] for i in range(len(consensusList))]
      # scatterplot
      plt.scatter(positionList, consensusList)
    # generate ticks
    ticks = list(range(len(patientGroup)))

    plt.xticks(ticks, patientGroup)

    plt.show()

scatterPlot()