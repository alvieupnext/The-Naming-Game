import networkx as nx
import numpy as np
import pandas as pd
from graphAnalysis.smallWorldNess import *
from patients.patientData import *

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

# addGraphMetadata(brumeg_functional_matrices, brumeg_functional_data).to_csv(here + 'BRUMEG_AAL2_functional_data_with_metadata.csv')