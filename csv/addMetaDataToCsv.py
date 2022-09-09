import pandas as pd
from patientData import *
import bct
from graphAnalysis.smallWorldNess import *

patientData = pd.read_csv('output/HPC_NetMats2_absolute.csv', index_col=0)

patients = loadHPCData("netmats2")

df = pd.DataFrame(columns=["subject", "characteristicPathLength", "globalEfficiency", "localEfficiency", "degreeDistribution", "clusterCoefficient", "transitivity", "smallWorldNess"])

for index, patient in enumerate(patients):
  charpath = bct.charpath(patient)
  characteristicPathLength = charpath[0]
  globalEfficiency = charpath[1]
  localEfficiency = bct.efficiency_wei(patient)
  degreeDistribution = np.mean(bct.strengths_und(patient))
  clusterCoefficient = np.mean(bct.clustering_coef_wu(patient))
  transitivity = np.mean(bct.transitivity_wu(patient))
  smallWorld = smallWorldNess(clusterCoefficient, characteristicPathLength)
  row = [index, characteristicPathLength, globalEfficiency, localEfficiency, degreeDistribution, clusterCoefficient, transitivity, smallWorld]
  df.loc[len(df.index)] = row

df["subject"] = df["subject"].astype(int)

merged = pd.merge(patientData, df)

print(df)

#
# patientData["MS"] = patientData["subject"].isin(MS_patients)
#
# print(SDMT)
#
# print(patientData)

merged.to_csv('output/HPC_NetMats2_absolute_with_MetaData.csv')