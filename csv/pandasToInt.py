import pandas as pd

patientData = pd.read_csv('output/convergencePerPatient(N_back_Reduced)_weighted_hydra_1000.csv', index_col=0)

new = patientData.astype(dtype=int, copy=True)

new.to_csv('output/convergencePerPatient(N_back_Reduced)_weighted_hydra_1000_int.csv')