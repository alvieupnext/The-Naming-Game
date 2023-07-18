
from patientData import *
from variants.ABNG import *
from functools import reduce
import pandas as pd
from MatrixFactory import *

columns = []

noOfAgents =100

population = loadHPCData("netmats2")

names = [i for i in range(len(population))]


for n in range(noOfAgents):
  for i in range(n):
    columns.append(f"C{n}-{i}")

print(columns)

df = pd.DataFrame(columns=columns, dtype=float)

for matrix, name in zip(population, names):
  #turn into binary array
  array = convertMatrixToArray(matrix)
  # #add patient at the start of the list
  # array.insert(0, name)
  # add row to dataframe
  df.loc[len(df.index)] = array

df.to_csv("output/HPC_NetMats2_v3.csv")

