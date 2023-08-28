from matplotlib import pyplot as plt
from variants.ABNG import *
from namingGameTools import Strategy, MatrixFactory as mf
import numpy as np

def map_choices(choices):
  if len(choices) == 0:
    return 0
  elif len(choices) == 2:
    return 3
  elif choices[0] == 'A':
    return 1
  else:
    return 2


def preferredAction(ng, actionMatrix, sorted_indices=None):

  fig, ax = plt.subplots()
  numberMatrix = np.zeros(actionMatrix.shape)
  for x in range(actionMatrix.shape[0]):
    for y in range(actionMatrix.shape[1]):
      numberMatrix[x,y] = map_choices(actionMatrix[x,y])
  ax.set_title(f"Preferred Action per Agent per Iteration ({ng.strategy.__name__})")
  ax.set_ylabel("Games played per agent")
  ax.set_xlabel("Agents")
  # Or only show every nth label
  n = 5  # Show every 5th label
  if sorted_indices is not None:
    ax.set_xticks(np.arange(len(sorted_indices)))
    ax.set_xticklabels([i if j % n == 0 else '' for j, i in enumerate(sorted_indices)])
  heatmap = ax.imshow(numberMatrix)

  cbar = fig.colorbar(heatmap, ax=ax, values=[0, 1 ,2,3])

  cbar.ax.set_yticklabels(["", "Ignorant", "", "A", "", "B", "", "Both", ""])

  plt.show()

factory = mf.MatrixFactory(triangular=False)

lattice = factory.makeLatticeMatrix(100, 5)

scaleFree = factory.makeScaleFreeMatrix(100)

smallWorld = factory.makeSmallWorldMatrix(100,5, 3)

ab = ABNG(simulations=1, maxIterations=100, strategy=Strategy.multi, output=["preferredAction"], consensusScore=[1], display=False)

output = ab.start(smallWorld)["preferredAction"][0]


def degree(matrix):
  print(matrix)
  """Calculate the degree of each node in the graph."""
  return np.sum(matrix, axis=0)


def sort_by_degree(matrix, actionMatrix):
  """Sort nodes in the graph by their degree."""
  degrees = degree(matrix)
  sorted_indices = np.argsort(degrees)[::-1]  # Descending order
  print(sorted_indices)
  print(degrees)
  sorted_degrees = degrees[sorted_indices]  # Reorder the degrees
  sorted_matrix = matrix[sorted_indices, :]
  sorted_matrix = sorted_matrix[:, sorted_indices]
  actionMatrix = np.array(actionMatrix, dtype=object)  # Convert actionMatrix to a NumPy array
  sorted_actionMatrix = actionMatrix[:, sorted_indices]
  return sorted_matrix, sorted_actionMatrix, sorted_indices


sorted_smallWorld, sorted_output, sorted_indices = sort_by_degree(smallWorld, output)

print(output)

print(sorted_output)

preferredAction(ab, sorted_output, sorted_indices)



