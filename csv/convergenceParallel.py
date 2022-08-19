#This code is responsible for exporting NG convergence results to a csv file (using multicore)

import pandas as pd
import numpy as np
from patientData import *
import Strategy
from variants.ABNG import *
import ray
from functools import reduce

consensusScoreList = [0.8, 0.9,0.95, 0.98, 0.99, 1]

scoresStringList = [f'SC_{score}' for score in consensusScoreList]

columns = ['NG sim', 'subject']

patientNames = names

columns.extend(scoresStringList)

groupSize = 1

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

print(patientGroups)

@ray.remote
def getDataFromPatient(patientList):
  ng = ABNG(maxIterations=5000, simulations=10, strategy=Strategy.multi, output=["popularity", "consensus"],
            consensusScore=consensusScoreList, display=False)
  df = pd.DataFrame(columns=columns)
  for patient in patientList:
    print(f"Using Patient Data {patient}")
    data = readPatientData(patient)
    output = ng.start(data)
    consensusList = output["consensus"]
    print(consensusList)
    for sim, simValues in enumerate(consensusList):
      # extract the convergence values from the simValues
      reformattedSimValues = list(map(lambda set: set[1], simValues))
      # if the array isn't the right size, fill rest of space with max iterations (not converged)
      while len(reformattedSimValues) < len(consensusScoreList):
        reformattedSimValues.append(ng.maxIterations)
      # add simulation number and patient to an array
      row = [sim, patient]
      # extend it with the reformatted simulation values
      row.extend(reformattedSimValues)
      # add row to dataframe
      df.loc[len(df.index)] = row
  print(df)
  return df

patientDataRemotes = []
for patientChunk in patientGroups:
  patientDataRemotes.append(getDataFromPatient.remote(patientChunk))

results = ray.get(patientDataRemotes)

patientData = reduce(lambda  left,right: pd.merge(left,right, how='outer'), results)

print(patientData)
