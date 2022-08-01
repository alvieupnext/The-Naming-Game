from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
import MatrixFactory as mf
from variants.ABNG import *
import Strategy
def preferredAction(ng, actionMatrix):

  fig, ax = plt.subplots()
  numberMatrix = np.zeros(actionMatrix.shape)
  for x in range(actionMatrix.shape[0]):
    for y in range(actionMatrix.shape[1]):
      if len(actionMatrix[x,y]) == 0 :
        #indecisive
        numberMatrix[x,y] = 0
      elif len(actionMatrix[x,y]) == 2:
        numberMatrix[x,y] = 3
      elif actionMatrix[x,y][0] == 'A':
        numberMatrix[x, y] = 1
      else: numberMatrix[x, y] = 2
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

ab = ABNG(maxIterations=100, strategy=Strategy.multi, output=["preferredAction"], consensusScore=[0.8], display=True)

output = ab.start(scaleFree)["preferredAction"][1]

preferredAction(ab, output)



