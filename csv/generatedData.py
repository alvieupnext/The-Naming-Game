from multiprocessing import Pool
from patientData import *
from variants.ABNG import *
from MatrixFactory import *
from functools import reduce

populationCount = 10

numberOfAgents =40

factory = MatrixFactory(generateWeight=generateConnectionWeight)

population = factory.generateSmallWorldPopulation(populationCount, 40, 20)

names = [f"g{i}" for i in range(populationCount)]

print(names)

consensusScoreList = [0.8, 0.9, 0.95, 0.98, 0.99, 1]

scoresStringList = [f"SC_{score}" for score in consensusScoreList]

columns = ['NG sim', 'subject']

columns.extend(scoresStringList)

def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')

def getDataFromSmallWorld(pair):
  smallWorld = pair[0]
  name = pair[1]
  ng = ABNG(maxIterations=1000000, simulations=1, strategy=Strategy.multi, output=["popularity", "consensus"],
            consensusScore=consensusScoreList, display=False)
  df = pd.DataFrame(columns=columns)
  print(f"Using Generated Data {name}")
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
  print(f"Finished using patient data {name}")
  return df


if __name__ == "__main__":
  with Pool(4) as pool:
    dataFrames = pool.map(getDataFromSmallWorld, zip(population, names))
    patientData = reduce(mergeData, dataFrames)
    print(patientData)
    patientData.to_csv("output/convergencePerGeneratedPatient.csv")





