#This code is responsible for exporting NG convergence results to a csv file

from patients.patientData import *
from variants.ABNG import *

consensusScoreList = [0.8, 0.9,0.95, 0.98, 0.99, 1]

scoresStringList = [f'SC_{score}' for score in consensusScoreList]

columns = ['NG sim', 'subject']

columns.extend(scoresStringList)

df = pd.DataFrame(columns=columns)

patientNames = names

ng = ABNG(maxIterations=5000, simulations=10, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=consensusScoreList, display=False)

for patient in patientNames:
  print(f"Using Patient Data {patient}")
  data = readPatientData(patient)
  output = ng.start(data)
  consensusList = output["consensus"]
  for sim, simValues in enumerate(consensusList):
    #extract the convergence values from the simValues
    reformattedSimValues = list(map(lambda set: set[1], simValues))
    #if the array isn't the right size, fill rest of space with NaN (not converged)
    while len(reformattedSimValues) < len(consensusScoreList):
      reformattedSimValues.append(ng.maxIterations)
    #add simulation number and patient to an array
    row = [sim, patient]
    #extend it with the reformatted simulation values
    row.extend(reformattedSimValues)
    #add row to dataframe
    df.loc[len(df.index)] = row
print(df)

#export to csv
df.to_csv("output/convergencePerPatient(N_back_Reduced)_weighted.csv")
