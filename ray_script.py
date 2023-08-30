#!/usr/bin/env python

from patients.patientData import *
from variants.ABNG import *
import ray

numberOfAgents = 100

consensusScoreList = [0.7, 0.8, 0.9, 0.95, 0.98, 0.99, 1]

scoresStringList = [f"SC_{score}" for score in consensusScoreList]

columns = ['NG sim', 'Subject']

columns.extend(scoresStringList)

#Get the names from lowesthighestpatients.txt comma seperated
names = [int(name) for name in open("patients/HCP/lowesthighestpatients.txt").read().split(",")]

# csv_data = pd.read_csv("csv_results/output/HCP_abs_v4.csv_results")
#
#
# # The patient IDs in the CSV file are integers, while the IDs we read from the text file are strings.
# # Let's convert the IDs in the CSV file to strings to make comparison easier.
#
# csv_patient_ids = csv_data["Subject"].astype(int).tolist()

def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')

def find_connected_components(smallWorld):
    n = len(smallWorld)
    visited = [False] * n

    def dfs(v):
      visited[v] = True
      for i in range(n):
        if i != v and (smallWorld[i][v] > 0 or smallWorld[v][i] > 0) and not visited[i]:
          dfs(i)

    components = 0
    for i in range(n):
      if not visited[i]:
        dfs(i)
        components += 1

    return components


def complete_matrix(triangular_matrix):
  n = len(triangular_matrix)
  complete = [[0] * n for _ in range(n)]
  for i in range(n):
    for j in range(i, n):
      complete[i][j] = triangular_matrix[i][j] if j < len(triangular_matrix[i]) else 0
      complete[j][i] = complete[i][j]
  return complete


@ray.remote
def getDataFromHospital(name):
  ng = ABNG(maxIterations=1000000, simulations=25, strategy=Strategy.mono, output=["popularity", "consensus"],
            consensusScore=consensusScoreList, display=True)
  df = pd.DataFrame(columns=columns, dtype=int)
  print(f"Using Hospital Data {name}")
  array = readCSVData("HCP_with_subjects_abs", name)
  smallWorld = convertArrayToMatrix(array, numberOfAgents)
  print(smallWorld)
  # smallWorld_complete = complete_matrix(smallWorld)
  # components = find_connected_components(smallWorld_complete)
  # print("Number of connected components:", components)
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
    patientData.to_csv("csv_results/output/convergenceHCPabs_25.csv_results")
















