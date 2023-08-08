from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
import MatrixFactory as mf
from variants.ABNG import *
import Strategy
from patientData import *


def map_choices(choices):
  if len(choices) == 0:
    return 0
  elif len(choices) == 2:
    return 3
  elif choices[0] == 'A':
    return 1
  else:
    return 2

from matplotlib.colors import ListedColormap

# Define the color map
color_dict = {0: 'lightgray', 1: 'blue', 2: 'yellow', 3: 'green'}
color_list = [color_dict[i] for i in range(4)]
cmap = ListedColormap(color_list)


def preferredAction(numberMatrix, sorted_indices=None):

  fig, ax = plt.subplots()
  # numberMatrix = np.zeros(actionMatrix.shape)
  # for x in range(actionMatrix.shape[0]):
  #   for y in range(actionMatrix.shape[1]):
  #     numberMatrix[x,y] = map_choices(actionMatrix[x,y])
  ax.set_title(f"Patient 102109, Preferred Action per Agent per Iteration (Mono)")
  ax.set_ylabel("Games played per agent")
  ax.set_xlabel("Agents")
  # Or only show every nth label
  n = 5  # Show every 5th label
  if sorted_indices is not None:
    ax.set_xticks(np.arange(len(sorted_indices)))
    ax.set_xticklabels([i if j % n == 0 else '' for j, i in enumerate(sorted_indices)])
  heatmap = ax.imshow(numberMatrix, aspect='auto', cmap=cmap)


  cbar = fig.colorbar(heatmap, ax=ax, values=[0, 1 ,2,3])

  cbar.ax.set_yticklabels(["", "Ignorant", "", "A", "", "B", "", "Both", ""])

  plt.show()

smallWorld = convertArrayToMatrix(readCSVData("HCP_with_subjects", 102109), 100)


def degree(matrix):
  """Calculate the degree of each node in the graph."""
  return np.sum(matrix, axis=0)

def triangular_to_full(matrix):
    """Convert a triangular matrix to a full adjacency matrix."""
    diagonal = np.diag(np.diag(matrix))  # Get the diagonal elements
    full_matrix = matrix + matrix.T - diagonal
    return full_matrix


import numpy as np

def sort_by_degree(matrix, actionMatrix):
    """Sort nodes in the graph by their degree."""
    # matrix = np.array(matrix)
    actionMatrix = np.array(actionMatrix, dtype=int)  # Convert actionMatrix to dtype=int
    degrees = degree(triangular_to_full(matrix))
    indices = np.arange(len(degrees))
    print(matrix)
    sorted_indices = np.argsort(degrees)[::-1]  # Descending order
    sorted_matrix = matrix[sorted_indices, :]
    sorted_matrix = sorted_matrix[:, sorted_indices]
    sorted_actionMatrix = actionMatrix[:, sorted_indices]
    return sorted_matrix, sorted_actionMatrix, sorted_indices


#load csv
csv = pd.read_csv('csv/output/convergenceHCP_1sim_preferred_action.csv', index_col=0)

#Get the only the rows with the subject number 102109
patientCSV = csv.loc[csv['Subject'] == 102109]

#Sort by ascending iteration
patientCSV = patientCSV.sort_values(by=['Iteration'])

#Remove iteration and subject columns
patientCSV = patientCSV.drop(columns=['Iteration', 'Subject'])

#Transform into a numpy matrix and remove the Iteration and Subject columns
output = patientCSV.to_numpy()






sorted_smallWorld, sorted_output, sorted_indices = sort_by_degree(smallWorld, output)

# print(sorted_output)


preferredAction(sorted_output, sorted_indices)



