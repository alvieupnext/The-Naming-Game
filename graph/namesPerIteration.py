from matplotlib import pyplot as plt
from BaselineNG import *
import MatrixFactory as mf
import Strategy

plt.title("Average Names In Circulation Per Iteration")

plt.xlabel("Games played per agent")

plt.ylabel("Amount of Names in Circulation")

factory = mf.MatrixFactory(triangular=True)

ng = BaselineNG(iterations=100, strategy=Strategy.mono)

yvalues = ng.start(factory.makeLatticeMatrix(40, 4))

plt.plot(yvalues)

plt.show()