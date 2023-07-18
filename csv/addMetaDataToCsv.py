from patientData import loadHPCData

import pandas as pd
import numpy as np
from graphAnalysis.smallWorldNess import *
import networkx as nx

# Load patient data from the CSV file
patientData = pd.read_csv('output/HPC_NetMats2_absolute.csv', index_col=0)

# Load patients' data from the patientData module (assuming it contains the necessary functions)
patients = loadHPCData("netmats2")

df = pd.DataFrame(
    columns=["subject", "characteristicPathLength", "globalEfficiency", "localEfficiency", "degreeDistribution",
             "clusterCoefficient", "transitivity", "smallWorldNess"])

for index, patient in enumerate(patients):
    print(patient)

    # Create an undirected weighted NetworkX graph from the patient's data
    graph = nx.from_numpy_array(patient)
    graph = graph.to_undirected()

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

    row = [index, characteristicPathLength, globalEfficiency, localEfficiency, degreeDistribution, clusterCoefficient,
           transitivity, smallWorld]
    df.loc[len(df.index)] = row

df["subject"] = df["subject"].astype(int)

merged = pd.merge(patientData, df)

print(df)

df.to_csv('output/HCP_NetMats2_MetaData_v2.csv')



