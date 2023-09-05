#procedure for turning patient code from csv_results into readable data
import numpy as np
import pandas as pd
import os

here = os.path.dirname(os.path.abspath(__file__))

def readFromPandasDataframe(df, number, mode = 'abs'):
    # Number coincides with the "Subject"  column
    desiredGenerated = df.loc[df['Subject'] == number]
    array = desiredGenerated.to_numpy()
    # #delete subject number
    ar_new = np.delete(array, 0)
    if mode == 'zero':
        # Make all negative numbers into a zero
        ar_new[ar_new < 0] = 0
    elif mode == 'abs':
        # Make all negative numbers into a positive
        ar_new = np.abs(ar_new)
    return ar_new

def getWeightsFromPatient(df, patient):
  #Get the row of the patient
  patientRow = df.loc[df["Subject"] == patient]
  #Turn the row into a numpy array
  patientArray = patientRow.to_numpy()
  #Delete the first element of the array (the patient number)
  patientArray = np.delete(patientArray, 0)
  #Return array
  return patientArray

#converts a lower triangular matrix into an array
def convertMatrixToArray(matrix):
  result = []
  for n in range(len(matrix)):
    for i in range(n):
      result.append(matrix[n, i])
  return result

#converts an array to a lower triangular matrix
def convertArrayToMatrix(array: object, noOfAgents: object) -> object:
  result = np.zeros((noOfAgents, noOfAgents), dtype=float)
  index = 0
  for n in range(noOfAgents):
    for i in range(n):
      result[n, i] = array[index]
      index += 1
  return result

def getConsensusIterationOfSubject(df, patient, convergenceRate, structure = 'SC'):
  patientRows = df.loc[df["Subject"] == patient]
  iterationRows = patientRows[f"{structure}_{convergenceRate}"]
  return iterationRows.tolist()




#Load the data from the folders
brumeg_functional_matrices = pd.read_csv(here + '/BRUMEG_functional/BRUMEG_AAL2_functional.csv')

brumeg_functional_data = pd.read_csv(here + '/BRUMEG_functional/BRUMEG_AAL2_functional_data.csv')

brumeg_functional_agents = 94

brumeg_functional_convergence = pd.read_csv(here + '/BRUMEG_functional/convergenceBRUMEG_AAL2_functional.csv')

# addGraphMetadata(brumeg_functional_matrices, brumeg_functional_data).to_csv(here + 'BRUMEG_AAL2_functional_data_with_metadata.csv')

hcp_patient_structural_matrices = pd.read_csv(here + '/HCP/HCP_NetMats2_v4.csv', index_col=0)

hcp_behavioral_data = pd.read_csv(here + '/HCP/behavioralInformation.csv')

hcp_convergence = pd.read_csv(here + '/HCP/convergenceHCP_abs_50.csv', index_col=0)

hcp_single_sim_preferred = pd.read_csv(here + '/HCP/convergenceHCP_1sim_preferred_action.csv', index_col=0)

# Reading the content of the file
with open(here + "/HCP/lowesthighestpatients.txt", "r") as file:
    content = file.read()

# Splitting the content into two groups based on newline
lowest_patients_str, highest_patients_str = content.split("\n")

# Separating the patients in each group using comma separator and converting them to integers
lowest_hcp_patients = [int(patient.strip()) for patient in lowest_patients_str.split(",") if patient.strip()]
highest_hcp_patients = [int(patient.strip()) for patient in highest_patients_str.split(",") if patient.strip()]



hcp_agents = 100

print(lowest_hcp_patients)

print(highest_hcp_patients)

# print(brumeg_functional_data.head())
# print(brumeg_functional_convergence.head())
#
# #Due to MATLAB workings, the first agent is 1, not 0
# print(brumeg_functional.head())
#
# print(hcp_patient_data.head())

