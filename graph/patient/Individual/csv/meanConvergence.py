from matplotlib import pyplot as plt
from patientData import *
from dataframeTools import *
import numpy as np

patientNames = list(range(812))

groupSize = len(patientNames) // 50

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

chosenConvergence = 0.95

def meanConvergence(name):
  path = here + f"/csv/output/{name}.csv"
  patientData = pd.read_csv(path)
  for i, patientGroup in enumerate(patientGroups):
    plt.title(f"Mean Plot Convergence with {chosenConvergence} with patient group {i}")
    plt.ylabel("Amount of Games played")
    plt.xlabel("Patient Number")
    #y values
    y = []
    for index, patient in enumerate(patientGroup):
      convergenceList = getConsensusIterationOfSubject(patientData, patient, chosenConvergence)
      y.append(np.mean(convergenceList))

    # generate x-positions
    x = list(range(len(patientGroup)))

    #set x-ticks
    plt.xticks(x, patientGroup)

    plt.plot(x, y)

    plt.show()


meanConvergence("convergenceHPC")
