#procedure for turning patient code from csv into readable data
import numpy as np
import pandas as pd
import random

import os

here = os.path.dirname(os.path.abspath(__file__))

# names = np.loadtxt(here + '/patients/names.csv', dtype=int)

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

def readCSVData(name, number, mode = 'zero', df = None):
  if df is None:
    # create file path
    path = here + f'/csv/output/{name}.csv'
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

#code for getting the neuron strenghts from a patient
def getWeightsFromPatient(name):
  #get matrix
  matrix = readPatientData(name)
  #turn into weight array and return
  return convertMatrixToArray(matrix)

# def getAllWeightsFromPatients():
#   weights = []
#   for patient in names:
#     weights.append(getWeightsFromPatient(patient))
#   return np.array(weights, dtype=float)

# weightDistribution = getAllWeightsFromPatients()

#choose a non-zero connection
# def generateConnectionWeight(frm, to):
#   #use the from and to to calculate the right connection in the array
#   #calculate difference between two (to always smaller)
#   difference = frm - to
#   #get sum of lists from 1 to frm
#   sumToFrm = (frm * (frm + 1))//2
#   #the weight neuron we need is the sumToFrm minus the difference
#   edge = sumToFrm - difference
#   #get the neuron weight from that neuron (should return a column of possible weights)
#   weights = weightDistribution[:, edge]
#   #choose one at random
#   weight, = random.choices(weights)
#   #get standard deviation from the weights (this will act as our noise) (comment this if you dont want noise)
#   std = np.std(weights)
#   #do not guess a negative weight
#   proposedWeight = random.uniform(max(weight - std, 0), weight + std)
#   return proposedWeight

def loadHPCData(name):
  #create file path
  path = here + f'/patients/hospital/{name}.txt'
  # get data from txt
  allPatients = np.loadtxt(path, dtype=float)
  #get absolute value from allPatients
  # allPatients = np.absolute(allPatients)
  allPatients[allPatients<0] = 0
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
# SDMT = pd.read_csv(here + '/patients/SDMT.csv')
#
# info = pd.read_csv(here + '/patients/info.csv')

# networkInfo = pd.read_csv(here + '/csv/output/NBackReducedPatientSC_with_MetaData.csv', index_col=0)
#
# convergenceInfo = pd.read_csv(here + '/csv/output/convergencePerPatient(N_back_Reduced)_weighted_hydra_1000_int.csv', index_col=0)

# info = info.loc[info["PatientNo"].isin(names)]

#get the patients that have MS and are in the names group
# MS = info.loc[info["MS"] == 1]
#
# MS_patients = MS["PatientNo"].tolist()
#
# control = info.loc[info["MS"] == 0]
#
# C_patients = control["PatientNo"].tolist()