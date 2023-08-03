from variants.ABNG import *
import Strategy
import ray
from patientData import *

hcp_names = pd.read_csv('csv/output/HCP_with_subjects.csv')
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
    ab = ABNG(simulations=1, maxIterations=100000, strategy=Strategy.mono, output=["preferredAction"],
            consensusScore=[1], display=False)
    numberOfAgents = 100
    matrix = convertArrayToMatrix(readCSVData("HCP_with_subjects", name), numberOfAgents)
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
  for name in hcp_names:
    patientDataRemotes.append(getDataFromHospital.remote(name))
  patientData = pd.DataFrame()
  while len(patientDataRemotes):
    doneRemote, patientDataRemotes = ray.wait(patientDataRemotes, timeout=None)
    print("Finished one")
    print("Remaing tasks: ", len(patientDataRemotes))
    patientData = mergeData(patientData, ray.get(doneRemote[0]))
    patientData.to_csv("csv/output/convergenceHCP_1sim_preferred_action.csv")

# df = getDataFromHospital(102109)
#
# df.to_csv("csv/output/convergenceHCP_1sim_preferred_action.csv")




# Load the patient_121921.csv from csv/output folder in pandas
# p121921_csv = pd.read_csv("csv/output/patient_121921.csv")
#
# # And patient_203923.csv
# p203923_csv = pd.read_csv("csv/output/patient_203923.csv")

# # Create a graph from the csvs (networkx)
# p121921 = nx.from_pandas_edgelist(p121921_csv, source="Source", target="Target", edge_attr="Weight")
# p203923 = nx.from_pandas_edgelist(p203923_csv, source="Source", target="Target", edge_attr="Weight")
#
# p121921_matrix = convertArrayToMatrix(readCSVData("HCP_with_subjects", 121921), numberOfAgents)
#
# p203923_matrix = convertArrayToMatrix(readCSVData("HCP_with_subjects", 203923), numberOfAgents)
#
# output = ab.start(p203923_matrix)["preferredAction"][0]
#
# print(output)
#
# preferredAction(ab, output, p203923)
