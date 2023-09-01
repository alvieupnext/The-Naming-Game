from variants.ABNG import *
from matplotlib import pyplot as plt

from patients.patientData import *

ng = ABNG(maxIterations=2000, simulations=10, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=[0.95], display=False)

patient_data = brumeg_functional_matrices

numberOfAgents = brumeg_functional_agents

#Get the patient names from the Subject column
patientNames = patient_data['Subject'].tolist()

#Only choose the first 4 patients
patientNames = patientNames[0:4]

# groupSize = len(patientNames) // 5
groupSize = 4

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

for i, patientGroup in enumerate(patientGroups):
  plt.title(
    f"Consensus Time Per Patient({ng.name}, {ng.simulations} simulations, using patient group {i} with size {groupSize})")

  plt.ylabel("Amount of Games played")

  plt.xlabel("Patient Number")

  for index, patient in enumerate(patientGroup):
    print(f"Using Patient Data {patient}")
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
      #if we reached convergence
      if consensusPerSimList:
        reformattedConsensusList.append(consensusPerSimList[0][1])
    print(reformattedConsensusList)
    #make a list of all positions (all to be scattered around the index)
    #generate a linear space from 0 to 1 to scatter points
    linspace = np.linspace(0., 1., len(reformattedConsensusList))
    positionList = [index - 0.5 + linspace[i] for i in range(len(reformattedConsensusList))]
    print(positionList)
    #scatterplot
    plt.scatter(positionList, reformattedConsensusList)

  #generate ticks
  ticks = list(range(len(patientGroup)))

  plt.xticks(ticks, patientGroup)

  plt.show()