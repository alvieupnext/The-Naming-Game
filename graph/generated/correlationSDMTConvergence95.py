from variants.ABNG import *
from matplotlib import pyplot as plt

from patients.patientData import *

ng = ABNG(maxIterations=2000, simulations=100, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=[0.95], display=False)

patientNames = names

groupSize = len(patientNames) // 1

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

for i, patientGroup in enumerate(patientGroups):
  plt.title(
    f"Correlation between {ng.consensusScore[-1]}Consensus Time And SMDT of Patient({ng.name}, {ng.simulations} simulations, using patient group {i} with size {groupSize})")

  plt.ylabel("SDMT score")

  plt.xlabel("Convergence Iteration")

#y value list,
  consensus = []

  for index, patient in enumerate(patientGroup):
    print(f"Using Patient Data {patient}")
    data = readPatientData(patient)
    output = ng.start(data)
    #list is only one element long, since we only converging at 0.95
    consensusList = output["consensus"]
    #reformat list to get the iteration values
    reformattedConsensusList = []
    # [0] to get the sole pair out of the list
    # [1] to get the iteration value
    for consensusPerSimList in consensusList:
      reformattedConsensusList.append(consensusPerSimList[0][1])
    consensus.append(np.mean(reformattedConsensusList))

  scores = SDMT["SDMT"].values[i:i+groupSize]

  print(consensus)

  print(scores)

 # plt.xcorr(consensus,scores)

  plt.scatter(consensus, scores)

  #generate ticks
  ticks = list(range(len(patientGroup)))

  # plt.xticks(ticks, patientGroup)

  plt.show()