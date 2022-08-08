from variants.ABNG import *
from matplotlib import pyplot as plt

ng = ABNG(maxIterations=2000, simulations=100, strategy=Strategy.multi, output=["popularity", "consensus"],
          consensusScore=[0.95], display=False)

plt.title(
  f"Consensus Time Per Neighbourhood Size({ng.name}, {ng.strategy.__name__}, {ng.simulations} simulations, using patient data)")

plt.ylabel("Amount of Games played")

plt.xlabel("Patient Number")