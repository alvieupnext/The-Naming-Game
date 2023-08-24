#procedure for turning patient code from csv into readable data
import numpy as np
import pandas as pd
import random

import os

here = os.path.dirname(os.path.abspath(__file__))

# names = np.loadtxt(here + '/patients/names.csv', dtype=int)

def readPatientData(name, type='connectivity'):
  #create file path
  path = here + f'/{type}/{name}.csv'
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

def readCSVData(name, number, mode = 'abs', dataset='BRUMEG', df = None):
  if df is None:
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

#Used for reading netmats files
def loadHPCData(name):
  #create file path
  path = here + f'/HCP/{name}.txt'
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