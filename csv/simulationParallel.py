# This code is responsible for testing parallel computing on the simulations
import sys
import os

sys.path.append('C:/Users/alvar/PycharmProjects/MAP')

import pandas as pd
import numpy as np
from multiprocessing import Pool
from patientData import *
import Strategy
from variants.ABNG import *
from functools import reduce

consensusScoreList = [0.8, 0.9, 0.95, 0.98, 0.99, 1]

scoresStringList = [f"SC_{score}" for score in consensusScoreList]

columns = ['NG sim', 'subject']

patientName = names[0]

columns.extend(scoresStringList)

groupSize = 1

df = pd.DataFrame(columns=columns)

totalSimulations = 10

maxIterations = 5000


def getSimDataFromPatient(patient):
  ng = ABNG(maxIterations=maxIterations, simulations=1, strategy=Strategy.multi, output=["popularity", "consensus"],
            consensusScore=consensusScoreList, display=False)
  print(f"Using Patient Data {patient}")
  data = readPatientData(patient)
  output = ng.start(data)
  consensusList = output["consensus"]
  return consensusList[0]


def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')

patientData = pd.DataFrame(columns=columns)



if __name__ == "__main__":
  with Pool(10) as pool:
    patientList = [patientName for i in range(totalSimulations)]
    simlists = pool.map(getSimDataFromPatient, patientList)
    reformattedSimValues = []
    for simlist in simlists:
      reformattedSim = list(map(lambda set: set[1], simlist))
      while len(reformattedSim) < len(consensusScoreList):
        reformattedSim.append(maxIterations)
      reformattedSimValues.append(reformattedSim)
    print(reformattedSimValues)

# if __name__ == "__main__":
#   ray.init()
#   try:
#     patientDataRemotes = []
#     for patientChunk in patientGroups:
#       patientDataRemotes.append(getDataFromPatient.remote(patientChunk))
#
#     patientData = pd.DataFrame(columns=columns)
#
#     while len(patientDataRemotes):
#       doneRemote, patientDataRemotes = ray.wait(patientDataRemotes, timeout=None)
#       print("Finished one")
#       patientData = mergeData(patientData, ray.get(doneRemote[0]))
#
#     patientData.to_csv("output/convergencePerPatient(N_back_Reduced)_weighted_2.csv")
#     print(patientData)
#   finally:
#     ray.shutdown()