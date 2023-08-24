from patients.patientData import *
from variants.ABNG import *
import ray

populationCount = 10000

numberOfAgents =40

names = [i for i in range(populationCount)]

consensusScoreList = [0.8, 0.9, 0.95, 0.98, 0.99, 1]

scoresStringList = [f"SC_{score}" for score in consensusScoreList]

columns = ['NG sim', 'subject']

columns.extend(scoresStringList)

def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')

@ray.remote
def getDataFromSmallWorld(name):
  ng = ABNG(maxIterations=1000000, simulations=100, strategy=Strategy.multi, output=["popularity", "consensus"],
            consensusScore=consensusScoreList, display=False)
  df = pd.DataFrame(columns=columns, dtype=int)
  print(f"Using Generated Data {name}")
  array = readCSVData("NBackReducedPatientSC_generated", name)
  smallWorld = convertArrayToMatrix(array, numberOfAgents)
  print(smallWorld)
  output = ng.start(smallWorld)
  consensusList = output["consensus"]
  for sim, simValues in enumerate(consensusList):
    # extract the convergence values from the simValues
    reformattedSimValues = list(map(lambda set: set[1], simValues))
    # if the array isn't the right size, fill rest of space with max iterations (not converged)
    while len(reformattedSimValues) < len(consensusScoreList):
      reformattedSimValues.append(ng.maxIterations)
    # add simulation number and patient to an array
    row = [sim, name]
    # extend it with the reformatted simulation values
    row.extend(reformattedSimValues)
    # add row to dataframe
    df.loc[len(df.index)] = row
  print(f"Finished using Generated patient data {name}")
  return df

getDataFromSmallWorld(1)


# if __name__ == "__main__":
#   with Pool(4) as pool:
#     dataFrames = pool.map(getDataFromSmallWorld, zip(population, names))
#     patientData = reduce(mergeData, dataFrames)
#     print(patientData)
#     patientData.to_csv("output/convergencePerGeneratedPatient.csv")

if __name__ == "__main__":
  ray.init(address='auto')
  patientDataRemotes = []
  for  name in names:
    patientDataRemotes.append(getDataFromSmallWorld.remote(name))

  patientData = pd.DataFrame(columns=columns, dtype=int)

  while len(patientDataRemotes):
    doneRemote, patientDataRemotes = ray.wait(patientDataRemotes, timeout=None)
    print("Finished one")
    patientData = mergeData(patientData, ray.get(doneRemote[0]))
    patientData.to_csv("csv/output/convergencePerPatient(N_back_Reduced)_Hydra_Ray_Generated.csv")





