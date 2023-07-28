from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
import MatrixFactory as mf
from variants.ABNG import *
import Strategy


def map_choices(choices):
  if len(choices) == 0:
    return 0
  elif len(choices) == 2:
    return 3
  elif choices[0] == 'A':
    return 1
  else:
    return 2


def preferredAction(ng, actionMatrix):

  fig, ax = plt.subplots()
  numberMatrix = np.zeros(actionMatrix.shape)
  for x in range(actionMatrix.shape[0]):
    for y in range(actionMatrix.shape[1]):
      numberMatrix[x,y] = map_choices(actionMatrix[x,y])
  ax.set_title(f"Preferred Action per Agent per Iteration ({ng.strategy.__name__})")
  ax.set_ylabel("Games played per agent")
  ax.set_xlabel("Agents")
  heatmap = ax.imshow(numberMatrix)

  cbar = fig.colorbar(heatmap, ax=ax, values=[0, 1 ,2,3])

  cbar.ax.set_yticklabels(["", "Ignorant", "", "A", "", "B", "", "Both", ""])

  plt.show()

factory = mf.MatrixFactory(triangular=True)

lattice = factory.makeLatticeMatrix(100, 5)

scaleFree = factory.makeScaleFreeMatrix(100)

smallWorld = factory.makeSmallWorldMatrix(100,5, 3)

ab = ABNG(simulations=1, maxIterations=100, strategy=Strategy.multi, output=["preferredAction"], consensusScore=[1], display=False)

output = ab.start(smallWorld)["preferredAction"][0]

print(output)

preferredAction(ab, output)



