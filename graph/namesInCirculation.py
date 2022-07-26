from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
from variants.ABNG import *
import MatrixFactory as mf
import Strategy

ng = ABNG(maxIterations=1000, simulations=10, strategy=Strategy.multi, output=["popularity"], consensusScore=0.8, display=False)

def namesInCirculation(popularity):
  plt.title(f"Proportion of names known by the Agents({ng.name}, {ng.strategy.__name__})")

  plt.xlabel("Games played per agent")

  plt.ylabel("Popularity of Name")


  allNames = list(popularity.keys())

  #to make sure we have the same legend every time
  allNames.sort()

  for name in allNames:
    yvalues = popularity[name]
    plt.plot(yvalues, label = name)

  plt.legend()



  plt.show()

factory = mf.MatrixFactory(triangular=True)

lattice = factory.makeLatticeMatrix(100, 5)

output = ng.start(lattice)

popularityPerSim = output["popularity"]

for popularity in popularityPerSim:
  namesInCirculation(popularity)