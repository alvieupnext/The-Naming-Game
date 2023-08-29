from patients.patientData import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

patientData = hcp_patient_data

agents = hcp_agents

patientNames = patientData['Subject'].tolist()



for index, patient in enumerate(patientNames[25:29]):
  data = getWeightsFromPatient(patientData, patient)
  matrix = convertArrayToMatrix(data, agents)
  mask = np.zeros_like(matrix)
  mask[np.triu_indices_from(mask)] = True
  plt.subplot(2, 2, index + 1)
  with sns.axes_style("white"):
    ax = sns.heatmap(matrix, mask=mask,  square=True,  cmap="YlGnBu")
    ax.set_title(patient, x=0.8, y=0.5)

plt.suptitle("Heatmaps Between The Nodes (HCP from NetMats2)")

plt.show()