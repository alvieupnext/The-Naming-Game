from variants.ABNG import *
import Strategy
import ray
from patientData import *

hcp_names = pd.read_csv('csv/output/BRUMEG_AAL2_functional.csv')
hcp_names = hcp_names['Subject'].tolist()

def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')


def map_choices(choices):
  if len(choices) == 0:
    return 0
  elif len(choices) == 2:
    return 3
  elif choices[0] == 'A':
    return 1
  else:
    return 2

@ray.remote
def getDataFromHospital(name):
    ab = ABNG(simulations=1, maxIterations=1000000, strategy=Strategy.mono, output=["preferredAction"],
            consensusScore=[1], display=False)
    numberOfAgents = 94
    matrix = convertArrayToMatrix(readCSVData("BRUMEG_AAL2_functional", name), numberOfAgents)
    output = ab.start(matrix)["preferredAction"][0]
    numberOutput = np.zeros((len(output), len(output[0])), dtype=int)
    #for every row in the output matrix
    for i in range(len(output)):
        #for every column in the row
        for j in range(len(output[i])):
            #if the value is not zero
            choices = output[i][j]
            numberOutput[i][j] = map_choices(choices)

    df = pd.DataFrame(numberOutput)

    #Add the index number as a seperate column called Iteration
    df['Iteration'] = df.index

    #Add the subject name to the dataframe
    df['Subject'] = name

    return df

if __name__ == "__main__":
  ray.init(address='auto')
  patientDataRemotes = []
  # Make an empty dataframe with all the columns we want (1 to 94, Iteration, Subject)
  patientData = pd.DataFrame(columns=list(range(94)), dtype=int)
  patientData['Iteration'] = patientData.index
  patientData['Subject'] = 0
  print(patientData)
  for name in hcp_names:
    patientDataRemotes.append(getDataFromHospital.remote(name))
  while len(patientDataRemotes):
    doneRemote, patientDataRemotes = ray.wait(patientDataRemotes, timeout=None)
    print("Finished one")
    print("Remaing tasks: ", len(patientDataRemotes))
    patientData = mergeData(patientData, ray.get(doneRemote[0]))
    patientData.to_csv("csv/output/convergenceBRUMEG_1sim_preferred_action.csv")