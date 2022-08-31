from patientData import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


for index,patient in enumerate(names[0:16]):
  data = readPatientData(patient)
  mask = np.zeros_like(data)
  mask[np.triu_indices_from(mask)] = True
  plt.subplot(4, 4, index + 1)
  with sns.axes_style("white"):
    ax = sns.heatmap(data, mask=mask,  square=True,  cmap="YlGnBu")
    ax.set_title(patient, x=0.8, y=0.5)

plt.show()