from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
import MatrixFactory as mf
import Strategy

def namesPerIteration(ng, matrixNetwork):
  plt.title(f"Average Names Invented in Total Per Iteration ({ng.name}, {ng.strategy.__name__})")

  plt.xlabel("Games played per agent")

  plt.ylabel("Amount of Names Invented")

  output = ng.start(matrixNetwork)

  nameTable = output["names"]

  yvalues = np.mean(nameTable, axis=1)

  plt.plot(yvalues)

  plt.show()

factory = mf.MatrixFactory(triangular=True)

lattice = factory.makeLatticeMatrix(40, 4)

Baseline = BaselineNG(iterations=100, strategy=Strategy.mono, output=["names"])

imi = Imitation(iterations=100, strategy=Strategy.mono, output=["names"])

imi2 = Imitationv2(iterations=100, strategy=Strategy.mono, output=["names"])

namesPerIteration(Baseline, lattice)

namesPerIteration(imi, lattice)

namesPerIteration(imi2, lattice)