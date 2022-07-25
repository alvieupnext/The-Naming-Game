from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
import MatrixFactory as mf
import Strategy

def namesPerIteration(ng, matrixNetwork):
  plt.title(f"Average Names Invented in Total Per Iteration ({ng.name})")

  plt.xlabel("Games played per agent")

  plt.ylabel("Amount of Names Invented")

  yvalues = ng.start(matrixNetwork)

  plt.plot(yvalues)

  plt.show()

factory = mf.MatrixFactory(triangular=True)

lattice = factory.makeLatticeMatrix(40, 4)

Baseline = BaselineNG(iterations=100, strategy=Strategy.mono)

imi = Imitation(iterations=100, strategy=Strategy.mono)

imi2 = Imitationv2(iterations=100, strategy=Strategy.mono)

namesPerIteration(Baseline, lattice)

namesPerIteration(imi, lattice)

namesPerIteration(imi2, lattice)