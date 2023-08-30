from matplotlib import pyplot as plt
from patients.patientData import *
import numpy as np

patientData = brumeg_functional_convergence

patientNames = patientData['Subject'].unique().tolist()

# groupSize = len(patientNames) // 50
groupSize = 5

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

chosenConvergence = 0.95

def meanConvergence():
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
