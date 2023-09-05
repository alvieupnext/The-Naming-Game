#!/usr/bin/env python

#Example on how to use the Naming Game and patient data using a script in Ray which then can be queued on a computer with multiple cores

from patients.patientData import *
from variants.ABNG import *
import ray
from patients.patientData import *

numberOfAgents = 100

consensusScoreList = [0.7, 0.8, 0.9, 0.95, 0.98, 0.99, 1]

scoresStringList = [f"SC_{score}" for score in consensusScoreList]

columns = ['NG sim', 'Subject']

columns.extend(scoresStringList)

#Get the names from lowesthighestpatients.txt comma seperated

lowest = lowest_hcp_patients
highest = highest_hcp_patients

#take names from both
names = lowest + highest
print(names)

data = hcp_patient_structural_matrices

def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')

@ray.remote
def getDataFromHospital(name):
  ng = ABNG(maxIterations=1000000, simulations=25, strategy=Strategy.mono, output=["popularity", "consensus"],
            consensusScore=consensusScoreList, display=True)
  df = pd.DataFrame(columns=columns, dtype=int)
  print(f"Using Hospital Data {name}")
  array = readFromPandasDataframe(data, name)
  smallWorld = convertArrayToMatrix(array, numberOfAgents)
  print(smallWorld)
  output = ng.start(smallWorld)
  consensusList = output["consensus"]
  for sim, simValues in enumerate(consensusList):
    # extract the convergence values from the simValues
    reformattedSimValues = list(map(lambda set: set[1], simValues))
    # if the array isn't the right size, fill rest of space with max iterations (not converged)
    while len(reformattedSimValues) < len(consensusScoreList):
      reformattedSimValues.append(ng.maxIterations)
    # add simulation number and patient to an array
    row = [sim, name]
    # extend it with the reformatted simulation values
    row.extend(reformattedSimValues)
    # add row to dataframe
    df.loc[len(df.index)] = row
  print(f"Finished using patient data {name}")
  return df


if __name__ == "__main__":
  ray.init(address='auto')
  patientDataRemotes = []
  for name in names:
    patientDataRemotes.append(getDataFromHospital.remote(name))
  patientData = pd.DataFrame(columns=columns, dtype=int)
  while len(patientDataRemotes):
    doneRemote, patientDataRemotes = ray.wait(patientDataRemotes, timeout=None)
    print("Finished one")
    print("Remaing tasks: ", len(patientDataRemotes))
    patientData = mergeData(patientData, ray.get(doneRemote[0]))
    patientData.to_csv("patients/output/convergenceHCPabs_25.csv_results")
















