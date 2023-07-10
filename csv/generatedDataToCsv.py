
from patientData import *
from variants.ABNG import *
from functools import reduce
import pandas as pd
from MatrixFactory import *

columns = ['subject']

populationCount = 10000

noOfAgents =40

print(noOfAgents)

factory = MatrixFactory(generateWeight=generateConnectionWeight)

population = factory.generateSmallWorldPopulation(populationCount, noOfAgents, 20)

names = [i for i in range(populationCount)]


for n in range(noOfAgents):
  for i in range(n):
    columns.append(f"C{n}-{i}")

df = pd.DataFrame(columns=columns, dtype=float)

for smallWorld,name in zip(population, names):
  #turn into binary array
  array = convertMatrixToArray(smallWorld)
  #add patient at the start of the list
  array.insert(0, name)
  # add row to dataframe
  df.loc[len(df.index)] = array

df["subject"] = df["subject"].astype(int)

print(df)

df.to_csv("output/NBackReducedPatientSC_generated.csv")

