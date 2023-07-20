#!/usr/bin/env python

from patientData import *
from variants.ABNG import *
import ray

numberOfAgents =100

consensusScoreList = [0.7, 0.8, 0.9, 0.95, 0.98, 0.99, 1]

scoresStringList = [f"SC_{score}" for score in consensusScoreList]

columns = ['NG sim', 'subject']

columns.extend(scoresStringList)

#Get the names from lowesthighestpatients.txt comma seperated
names = [int(name) for name in open("lowesthighestpatients.txt").read().split(",")]

# names = list(range(812))]

print(len(names))

def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')

@ray.remote
def getDataFromHospital(name):
  ng = ABNG(maxIterations=10000, simulations=15, strategy=Strategy.mono, output=["popularity", "consensus"],
            consensusScore=consensusScoreList, display=False)
  df = pd.DataFrame(columns=columns, dtype=int)
  print(f"Using Hospital Data {name}")
  array = readCSVData("HCP_with_subjects", name)
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
  # print(getDataFromHospital(102109))
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
    patientData.to_csv("csv/output/convergenceHCP_20percent_15_2ndpart.csv")
















