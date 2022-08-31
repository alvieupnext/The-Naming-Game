from matplotlib import pyplot as plt
from patientData import *
import pandas as pd
from dataframeTools import *

#this graph will use the csv provided in csv/outputs

consensusScoreList = [0.8, 0.9,0.95, 0.98, 0.99, 1]

# we are interested in the 10% highest convergence
proportion = 0.1

def generateScatterPlot(name):
  path = here + f"/csv/output/{name}.csv"
  patientData = pd.read_csv(path)
  for consensusScore in consensusScoreList:
    plt.title(
      f"Top {proportion * 100}% mean convergence, consensus at {consensusScore})")

    plt.ylabel("Amount of Games played")

    MS_list = []
    C_list = []
    for patient in names:
      consensus = getConsensusIterationOfSubject(patientData, patient, consensusScore)
      consensus = np.array(consensus, dtype=int)
      sortedIndexConsensus = np.argsort(consensus)
      sortedConsensus = consensus[sortedIndexConsensus]
      proportionWeightCount = len(consensus) * proportion
      proportionWeightCount = int(proportionWeightCount)
      weights = sortedConsensus[-proportionWeightCount :]
      #calculate mean from the biggest weights
      mean = np.mean(weights)
      if patient in names:
        if patient in MS_patients:
          MS_list.append(mean)
        else:
          C_list.append(mean)
    for index, lst in enumerate([MS_list, C_list]):
      linspace = np.linspace(0., 1., len(lst))
      positionList = [index + 1 - 0.5 + linspace[i] for i in range(len(lst))]
      plt.scatter(positionList, lst)

    plt.xticks([1,2], ["MS", "Control"])

    plt.show()

generateScatterPlot("convergencePerPatient(N_back_Reduced)_weighted_hydra_1000")
