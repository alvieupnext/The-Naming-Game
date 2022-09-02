#procedure for turning patient code from csv into readable data
import numpy as np
import pandas as pd
import random

import os

here = os.path.dirname(os.path.abspath(__file__))

names = np.loadtxt(here + '/patients/names.csv', dtype=int)

def readPatientData(name, type='connectivity'):
  #create file path
  path = here + f'/patients/{type}/{name}.csv'
  #get data from csv
  array = np.loadtxt(path, delimiter=',', dtype=float)
  # numberOfAgents is the square root of the total array length
  numberOfAgents = np.sqrt(len(array)).astype(int)
  #turn data into the right array dimension
  matrix = np.reshape(array, (numberOfAgents, numberOfAgents))
  #fill matrix diagonal with 0s
  np.fill_diagonal(matrix, 0)
  #make matrix triangular and return
  return np.tril(matrix)

#converts a lower triangular matrix into an array
def convertMatrixToArray(matrix):
  result = []
  for n in range(len(matrix)):
    for i in range(n):
      result.append(matrix[n, i])
  return result

#code for getting the neuron strenghts from a patient
def getWeightsFromPatient(name):
  #get matrix
  matrix = readPatientData(name)
  #turn into weight array and return
  return convertMatrixToArray(matrix)

def getAllWeightsFromPatients():
  weights = []
  for patient in names:
    weights.append(getWeightsFromPatient(patient))
  return np.array(weights, dtype=float)

weightDistribution = getAllWeightsFromPatients()

#choose a non-zero connection
def generateConnectionWeight(frm, to):
  print(weightDistribution)
  #use the from and to to calculate the right connection in the array
  #calculate difference between two (to always smaller)
  difference = frm - to
  #get sum of lists from 1 to frm
  sumToFrm = (frm * (frm + 1))//2
  #the weight neuron we need is the sumToFrm minus the difference
  edge = sumToFrm - difference
  #get the neuron weight from that neuron (should return a column of possible weights)
  weights = weightDistribution[:, edge]
  #choose one at random
  weight, = random.choices(weights)
  return weight


# def readPatientData(name, type='connectivity'):
#   #get data from csv
#   array = np.loadtxt(f'../patients/{type}/{name}.csv', delimiter=',', dtype=float)
#   # numberOfAgents is the square root of the total array length
#   numberOfAgents = np.sqrt(len(array)).astype(int)
#   #threshold
#   def binary(el):
#     if el >= 1:
#       return 1
#     else: return 0
#   #change values into either 0 or 1 (could be removed later)
#   binaryArray = list(map(binary, array))
#   #turn data into the right array dimension
#   matrix = np.reshape(binaryArray, (numberOfAgents, numberOfAgents))
#   #make the matrix triangular
#   trig = np.tril(matrix)
#   #fill the main diagonal with 0s
#   np.fill_diagonal(trig, 0)
#   return trig
# #
SDMT = pd.read_csv(here + '/patients/SDMT.csv')

info = pd.read_csv(here + '/patients/info.csv')

networkInfo = pd.read_csv(here + '/csv/output/NBackReducedPatientSC_with_MetaData.csv', index_col=0)

convergenceInfo = pd.read_csv(here + '/csv/output/convergencePerPatient(N_back_Reduced)_weighted_hydra_1000_int.csv', index_col=0)

info = info.loc[info["PatientNo"].isin(names)]

#get the patients that have MS and are in the names group
MS = info.loc[info["MS"] == 1]

MS_patients = MS["PatientNo"].tolist()

control = info.loc[info["MS"] == 0]

C_patients = control["PatientNo"].tolist()

print(getWeightsFromPatient("2096"))