from variants.ABNG import *
import ray
from patients.patientData import *

def mergeData(sum, df):
  return pd.merge(sum, df, how='outer')

numberOfAgents = brumeg_functional_agents

data = brumeg_functional_matrices

#Get the names from Subject column in data
names = data['Subject'].unique()


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
    matrix = convertArrayToMatrix(readFromPandasDataframe(data, name), numberOfAgents)
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
  for name in names:
    patientDataRemotes.append(getDataFromHospital.remote(name))
  while len(patientDataRemotes):
    doneRemote, patientDataRemotes = ray.wait(patientDataRemotes, timeout=None)
    print("Finished one")
    print("Remaing tasks: ", len(patientDataRemotes))
    patientData = mergeData(patientData, ray.get(doneRemote[0]))
    patientData.to_csv("patients/output/convergenceBRUMEG_1sim_preferred_action.csv")