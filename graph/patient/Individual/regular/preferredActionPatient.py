from matplotlib import pyplot as plt
from patients.patientData import *
from variants.ABNG import *
from namingGameTools import Strategy

ng = ABNG(maxIterations=100, simulations=1, strategy=Strategy.multi, output=["preferredAction"],
          consensusScore=[0.95], display=False)

patient_data = brumeg_functional
numberOfAgents = brumeg_functional_agents
patient = 1


data = readFromPandasDataframe(patient_data, patient)
matrix = convertArrayToMatrix(data, numberOfAgents)

output = ng.start(matrix)

actionMatrix = output["preferredAction"][0]

fig, ax = plt.subplots()
shape = len(actionMatrix), len(actionMatrix[0])
print(shape)
numberMatrix = np.zeros(shape)
for x in range(shape[0]):
  for y in range(shape[1]):
    if len(actionMatrix[x][y]) == 0:
      # indecisive
      numberMatrix[x, y] = 0
    elif len(actionMatrix[x][y]) == 2:
      numberMatrix[x, y] = 3
    elif actionMatrix[x][y][0] == 'A':
      numberMatrix[x, y] = 1
    else:
      numberMatrix[x, y] = 2
ax.set_title(f"Preferred Action per Agent per Iteration ({ng.strategy.__name__})")
ax.set_ylabel("Games played per agent")
ax.set_xlabel("Agents")
heatmap = ax.imshow(numberMatrix)

cbar = fig.colorbar(heatmap, ax=ax, values=[0, 1, 2, 3])

cbar.ax.set_yticklabels(["", "Ignorant", "", "A", "", "B", "", "Both", ""])

plt.show()