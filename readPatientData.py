#procedure for turning patient code from csv into readable data
import numpy as np
import pandas as pd

def readPatientData(name, numberOfAgents, type='connectivity'):
  #get data from csv
  array = np.loadtxt(f'../patients/{type}/{name}.csv', delimiter=',', dtype=float)
  def binary(el):
    if el:
      return 1
    else: return 0
  #change values into either 0 or 1 (could be removed later)
  binaryArray = list(map(binary, array))
  #turn data into the right array dimension
  matrix = np.reshape(binaryArray, (numberOfAgents, numberOfAgents))
  #make the matrix triangular
  trig = np.tril(matrix)
  #fill the main diagonal with 0s
  np.fill_diagonal(trig, 0)
  return trig

names = np.loadtxt(f'../patients/names.csv', dtype=int)

# print(readPatientData("2096", 40))