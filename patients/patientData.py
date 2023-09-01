#procedure for turning patient code from csv_results into readable data
import numpy as np
import pandas as pd
import networkx as nx
from graphAnalysis.smallWorldNess import *
import random

import os

here = os.path.dirname(os.path.abspath(__file__))

# names = np.loadtxt(here + '/patients/names.csv_results', dtype=int)

def readCSVData(name, number, mode = 'abs', dataset='BRUMEG'):
  # create file path
  path = here + f'/patient/{dataset}/{name}.csv_results'
  # get data from csv_results
  df = pd.read_csv(path)
  # Number coincides with the "Subject"  column
  desiredGenerated = df.loc[df['Subject'] == number]
  array = desiredGenerated.to_numpy()
  # #delete subject number
  ar_new = np.delete(array, 0)
  if mode == 'zero':
    # Make all negative numbers into a zero
    ar_new[ar_new < 0] = 0
  elif mode == 'abs':
    # Make all negative numbers into a positive
    ar_new = np.abs(ar_new)
  return ar_new

def readFromPandasDataframe(df, number, mode = 'abs'):
    # Number coincides with the "Subject"  column
    desiredGenerated = df.loc[df['Subject'] == number]
    array = desiredGenerated.to_numpy()
    # #delete subject number
    ar_new = np.delete(array, 0)
    if mode == 'zero':
        # Make all negative numbers into a zero
        ar_new[ar_new < 0] = 0
    elif mode == 'abs':
        # Make all negative numbers into a positive
        ar_new = np.abs(ar_new)
    return ar_new

def getWeightsFromPatient(df, patient):
  #Get the row of the patient
  patientRow = df.loc[df["Subject"] == patient]
  #Turn the row into a numpy array
  patientArray = patientRow.to_numpy()
  #Delete the first element of the array (the patient number)
  patientArray = np.delete(patientArray, 0)
  #Return array
  return patientArray

#converts a lower triangular matrix into an array
def convertMatrixToArray(matrix):
  result = []
  for n in range(len(matrix)):
    for i in range(n):
      result.append(matrix[n, i])
  return result

#converts an array to a lower triangular matrix
def convertArrayToMatrix(array: object, noOfAgents: object) -> object:
  result = np.zeros((noOfAgents, noOfAgents), dtype=float)
  index = 0
  for n in range(noOfAgents):
    for i in range(n):
      result[n, i] = array[index]
      index += 1
  return result

def getConsensusIterationOfSubject(df, patient, convergenceRate, structure = 'SC'):
  patientRows = df.loc[df["Subject"] == patient]
  iterationRows = patientRows[f"{structure}_{convergenceRate}"]
  return iterationRows.tolist()

#Make an NetworkX graph from a patient and given a dataframe
def createGraphFromSubjectNumber(subject_number, data):
  """Create a NetworkX graph for a given subject number from the dataset."""
  row = data[data["Subject"] == subject_number].iloc[0].drop("Subject")

  graph = nx.Graph()

  for col, weight in row.items():
    if '-' in col and weight != 0:
      source, target = map(int, col[1:].split('-'))
      graph.add_edge(source, target, Weight=np.abs(weight))

  return graph

#Add graphMetadata to the patientData
def addGraphMetadata(structuralData, patientData):
  df = pd.DataFrame(
    columns=["Subject", "characteristicPathLength", "globalEfficiency", "localEfficiency", "degreeDistribution",
             "clusterCoefficient", "transitivity", "smallWorldNess"
             ])
  #get all Subject names from the structuralData
  subjectNames = structuralData["Subject"].tolist()
  for patient in subjectNames:
    print(f"Adding metadata to patient {patient}")
    #get the graph from the patient
    graph = createGraphFromSubjectNumber(patient, structuralData)
    assert(not graph.is_directed())
    # Calculate characteristic path length and global efficiency
    characteristicPathLength = nx.average_shortest_path_length(graph)
    globalEfficiency = nx.global_efficiency(graph)

    # Calculate local efficiency
    localEfficiency = nx.local_efficiency(graph)

    # Calculate degree distribution
    degreeDistribution = np.mean([d for _, d in graph.degree()])

    # Calculate cluster coefficient
    clusterCoefficient = nx.average_clustering(graph)

    # Calculate transitivity
    transitivity = nx.transitivity(graph)

    # Calculate small-worldness using bctpy
    smallWorld = smallWorldNess(clusterCoefficient, characteristicPathLength)

    row = [patient, characteristicPathLength, globalEfficiency, localEfficiency, degreeDistribution,
           clusterCoefficient,transitivity, smallWorld
           ]

    #Insert row to dataframe
    df.loc[len(df)] = row

  #Merge the dataframe with the patientData
  return pd.merge(patientData, df, on="Subject")




#Load the data from the folders
brumeg_functional_matrices = pd.read_csv(here + '/BRUMEG_functional/BRUMEG_AAL2_functional.csv')

brumeg_functional_data = pd.read_csv(here + '/BRUMEG_functional/BRUMEG_AAL2_functional_data.csv')

brumeg_functional_agents = 94

brumeg_functional_convergence = pd.read_csv(here + '/BRUMEG_functional/convergenceBRUMEG_AAL2_functional.csv')

# print("busy")
#
# addGraphMetadata(brumeg_functional_matrices, brumeg_functional_data).to_csv(here + 'BRUMEG_AAL2_functional_data_with_metadata.csv')

hcp_patient_structural_matrices = pd.read_csv(here + '/HCP/HCP_NetMats2_v4.csv', index_col=0)

hcp_behavioral_data = pd.read_csv(here + '/HCP/behavioralInformation.csv')

hcp_convergence = pd.read_csv(here + '/HCP/convergenceHCP_abs_50.csv', index_col=0)

hcp_single_sim_preferred = pd.read_csv(here + '/HCP/convergenceHCP_1sim_preferred_action.csv', index_col=0)


hcp_agents = 100

print(hcp_behavioral_data)

print(hcp_convergence)

# print(brumeg_functional_data.head())
# print(brumeg_functional_convergence.head())
#
# #Due to MATLAB workings, the first agent is 1, not 0
# print(brumeg_functional.head())
#
# print(hcp_patient_data.head())

