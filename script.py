# This code is responsible for exporting NG convergence results to a csv file (using multicore)

#This code is for running in the Hydra cluster

from multiprocessing import Pool
from patientData import *
from variants.ABNG import *
from functools import reduce
import ray

consensusScoreList = [0.8, 0.9, 0.95, 0.98, 0.99, 1]

scoresStringList = [f"SC_{score}" for score in consensusScoreList]

columns = ['NG sim', 'subject']

patientNames = names

columns.extend(scoresStringList)

groupSize = 1

patientGroups = [patientNames[i:i + groupSize] for i in range(0, len(patientNames), groupSize)]

@ray.remote
def getDataFromPatient(patientList):
  ng = ABNG(maxIterations=100000, simulations=1000, strategy=Strategy.multi, output=["popularity", "consensus"],
            consensusScore=consensusScoreList, display=False)
  df = pd.DataFrame(columns=columns)
  for patient in patientList:
    print(f"Using Patient Data {patient}")
    data = readPatientData(patient)
    output = ng.start(data)
    consensusList = output["consensus"]
    for sim, simValues in enumerate(consensusList):
      # extract the convergence values from the simValues
      reformattedSimValues = list(map(lambda set: set[1], simValues))
      # if the array isn't the right size, fill rest of space with max iterations (not converged)
      while len(reformattedSimValues) < len(consensusScoreList):
        reformattedSimValues.append(ng.maxIterations)
      # add simulation number and patient to an array
      row = [sim, patient]
      # extend it with the reformatted simulation values
      row.extend(reformattedSimValues)
      # add row to dataframe
      df.loc[len(df.index)] = row
    print(f"Finished using patient data {patient}")
  return df


def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')

patientData = pd.DataFrame(columns=columns)



# if __name__ == "__main__":
#   with Pool(10) as pool:
#     dataFrames = pool.map(getDataFromPatient, patientGroups)
#     patientData = reduce(mergeData, dataFrames)
#     print(patientData)
#     patientData.to_csv("output/convergencePerPatient(N_back_Reduced)_weighted_2.csv")

if __name__ == "__main__":
  ray.init()
  try:
    patientDataRemotes = []
    for patientChunk in patientGroups:
      patientDataRemotes.append(getDataFromPatient.remote(patientChunk))

    patientData = pd.DataFrame(columns=columns)

    while len(patientDataRemotes):
      doneRemote, patientDataRemotes = ray.wait(patientDataRemotes, timeout=None)
      print("Finished one")
      patientData = mergeData(patientData, ray.get(doneRemote[0]))
      patientData.to_csv("csv/output/convergencePerPatient(N_back_Reduced)_weighted_hydra_tussen.csv")
  finally:
    ray.shutdown()







