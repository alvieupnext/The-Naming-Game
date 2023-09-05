# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

import os
print(os.getcwd())

#Load from BRUMEG functional folder convergenceBRUMEG_AAL2_functional.csv_results
brumeg_aal2_functional_convergence = pd.read_csv("../output/convergenceBRUMEG_AAL2_abs_50.csv")

#Load from the same folder DATA_MEG1.csv_results
brumeg_aal2_functional_data = pd.read_csv("DATA_MEG1.csv")

#Rename from the data csv_results name to Subject
brumeg_aal2_functional_data.rename(columns={'name':'Subject'}, inplace=True)

#print the head of the dataframe
print(brumeg_aal2_functional_convergence.head())

#Export to csv_results
brumeg_aal2_functional_convergence.to_csv("convergenceBRUMEG_AAL2_functional.csv", index=False)

#Export to csv_results
brumeg_aal2_functional_data.to_csv("BRUMEG_AAL2_functional_data.csv", index=False)

