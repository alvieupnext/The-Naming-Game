
import os
import pandas as pd
import numpy as np
from patients.patientData import convertMatrixToArray

columns = []

noOfAgents =100

here = os.path.dirname(os.path.abspath(__file__))

#Used for reading netmats files
def loadHCPData(name):
  #create file path
  path = here + f'/{name}.txt'
  # get data from txt
  allPatients = np.loadtxt(path, dtype=float)
  #get absolute value from allPatients
  # allPatients = np.absolute(allPatients)
  # allPatients[allPatients<0] = 0
  print(allPatients.shape)
  # how many patients are there
  noOfPatients = len(allPatients)
  #how many elements does one patient contain
  noOfElements = len(allPatients[0])
  numberOfAgents = np.sqrt(noOfElements).astype(int)
  #generate list of matrices
  matrices = []
  #calculate number of agents
  for patient in allPatients:
    matrix = np.reshape(patient, (numberOfAgents, numberOfAgents))
    matrices.append(matrix)
  return matrices

population = loadHCPData("netmats2")

names = [i for i in range(len(population))]


for n in range(noOfAgents):
  for i in range(n):
    columns.append(f"C{n}-{i}")

print(columns)

hcp_dataframe_100nodes = pd.DataFrame(columns=columns, dtype=float)

for matrix, name in zip(population, names):
  #turn into binary array
  array = convertMatrixToArray(matrix)
  # #add patient at the start of the list
  # array.insert(0, name)
  # add row to dataframe
  hcp_dataframe_100nodes.loc[len(hcp_dataframe_100nodes.index)] = array

#Load the subjects from subjects.txt
subjects = np.loadtxt(here + '/subjects.txt', dtype=int)

#Add the subjects to the dataframe
hcp_dataframe_100nodes.insert(0, "Subject", subjects)

hcp_dataframe_100nodes.to_csv("HCP_NetMats2_v4.csv")

