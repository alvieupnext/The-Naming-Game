#procedure for turning patient code from csv into readable data
import numpy as np
import pandas as pd
import random

import os

here = os.path.dirname(os.path.abspath(__file__))

# names = np.loadtxt(here + '/patients/names.csv', dtype=int)

def readCSVData(name, number, mode = 'abs', dataset='BRUMEG'):
  # create file path
  path = here + f'/patient/{dataset}/{name}.csv'
  # get data from csv
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


#Load the data from the folders
brumeg_functional = pd.read_csv(here + '/BRUMEG_functional/BRUMEG_AAL2_functional.csv')

brumeg_functional_data = pd.read_csv(here + '/BRUMEG_functional/BRUMEG_AAL2_functional_data.csv')

brumeg_functional_agents = 94

brumeg_functional_convergence = pd.read_csv(here + '/BRUMEG_functional/convergenceBRUMEG_AAL2_functional.csv')

hcp_patient_data = pd.read_csv(here + '/HCP/HCP_NetMats2_v4.csv', index_col=0)

hcp_agents = 100


print(brumeg_functional_data.head())
# print(brumeg_functional_convergence.head())
#
# #Due to MATLAB workings, the first agent is 1, not 0
# print(brumeg_functional.head())
#
# print(hcp_patient_data.head())

