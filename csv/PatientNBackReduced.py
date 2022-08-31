
from patientData import *
from variants.ABNG import *
from functools import reduce
import pandas as pd

columns = ['subject']

patientNames = names

firstName = patientNames[0]

noOfAgents = len(readPatientData(firstName))

print(noOfAgents)

for n in range(noOfAgents):
  for i in range(n):
    columns.append(f"C{n}-{i}")

#converts a lower triangular matrix into an array
def convertMatrixToArray(matrix):
  result = []
  for n in range(len(matrix)):
    for i in range(n):
      result.append(matrix[n, i])
  return result

df = pd.DataFrame(columns=columns, dtype=float)

for patient in patientNames:
  matrix = readPatientData(patient)
  #turn into binary array
  array = convertMatrixToArray(matrix)
  #add patient at the start of the list
  array.insert(0, patient)
  # add row to dataframe
  df.loc[len(df.index)] = array

df["subject"] = df["subject"].astype(int)

print(df)

df.to_csv("output/NBackReducedPatientSC.csv")

