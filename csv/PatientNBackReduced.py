
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

