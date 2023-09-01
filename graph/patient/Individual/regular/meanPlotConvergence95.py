from variants.ABNG import *
from matplotlib import pyplot as plt

from patients.patientData import *

ng = ABNG(maxIterations=2000, simulations=3, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=[0.95], display=False)

patient_data = brumeg_functional_matrices

numberOfAgents = brumeg_functional_agents

#Get the patient names from the Subject column
patientNames = patient_data['Subject'].tolist()

# For only choosing a subset of patients
patientNames = patientNames[0:4]

# groupSize = len(patientNames) // 5
groupSize = 4

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

for i, patientGroup in enumerate(patientGroups):
  plt.title(
    f"Consensus Time Per Patient({ng.name}, {ng.simulations} simulations, using patient group {i} with size {groupSize})")

  plt.ylabel("Amount of Games played")

  plt.xlabel("Patient Number")

  y = []

  for index, patient in enumerate(patientGroup):
    print(f"Using Patient Data {patient}")
    #Get the patient data from the pandas
    data = readFromPandasDataframe(patient_data, patient)
    matrix = convertArrayToMatrix(data, numberOfAgents)
    output = ng.start(matrix)
    #list is only one element long, since we only converging at 0.95
    consensusList = output["consensus"]
    #reformat list to get the iteration values
    reformattedConsensusList = []
    # [0] to get the sole pair out of the list
    # [1] to get the iteration value
    for consensusPerSimList in consensusList:
      if consensusPerSimList:
        reformattedConsensusList.append(consensusPerSimList[0][1])
    print(reformattedConsensusList)
    y.append(np.mean(reformattedConsensusList))

  # generate x-positions
  x = list(range(len(patientGroup)))

  plt.plot(x, y)

  plt.xticks(x, patientGroup)

  plt.show()