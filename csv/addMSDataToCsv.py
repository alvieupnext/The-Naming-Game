import pandas as pd
from patientData import *

patientData = pd.read_csv('output/convergencePerPatient(N_back_Reduced)_weighted_hydra_1000.csv', index_col=0)

patientData["MS"] = patientData["subject"].isin(MS_patients)

print(patientData)

patientData.to_csv('output/convergencePerPatient(N_back_Reduced)_weighted_hydra_1000_with_MSData.csv',)