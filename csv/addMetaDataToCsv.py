import pandas as pd
from patientData import *

patientData = pd.read_csv('output/NBackReducedPatientSC.csv', index_col=0)

patientData["MS"] = patientData["subject"].isin(MS_patients)

patientData["SDMT"] = SDMT

print(SDMT)

print(patientData)

patientData.to_csv('output/NBackReducedPatientSC_with_MetaData.csv',)