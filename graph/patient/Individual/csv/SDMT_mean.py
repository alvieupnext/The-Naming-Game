from matplotlib import pyplot as plt

from patients.patientData import *
from dataframeTools import *
import numpy as np

chosenConvergence = 0.95

scoreArray = SDMT["SDMT"].values

def SMDT(name):
  path = here + f"/csv/output/{name}.csv"
  patientData = pd.read_csv(path)
  plt.title(f"Scatter Plot Convergence {chosenConvergence} and SDMT score (Mean Convergence)")
  plt.ylabel("Amount of Games played")
  plt.xlabel("SDMT score")
  MS_consensus = []
  MS_scores = []
  C_consensus = []
  C_scores = []
  for index, patient in enumerate(names):
    consensusList = getConsensusIterationOfSubject(patientData, patient, chosenConvergence)
    score = scoreArray[index]
    if patient in MS_patients:
      MS_consensus.append(np.mean(consensusList))
      MS_scores.append(score)
    else:
      C_consensus.append(np.mean(consensusList))
      C_scores.append(score)
  plt.scatter(MS_scores, MS_consensus, c='red', label="MS")

  plt.scatter(C_scores, C_consensus, c='blue', label="Control")

  plt.legend()

  plt.show()

SMDT("convergencePerPatient(N_back_Reduced)_weighted_hydra_1000")
