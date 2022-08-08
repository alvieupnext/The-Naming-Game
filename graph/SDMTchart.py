from matplotlib import pyplot as plt
import pandas as pd
from readPatientData import *



plt.title(f"SDMT chart")

plt.xlabel("Patients")

plt.ylabel("SDMT score")

dataTable = pd.read_csv('../patients/SDMT.csv')

patientNames = names

groupSize = len(names) // 5

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

for index, group in enumerate(patientGroups):
  plt.title(f"SDMT chart")

  plt.xlabel("Patients")

  plt.ylabel("SDMT score")

  data = dataTable['SDMT'][index*groupSize:index*groupSize + groupSize]



  print(data.values)

  plt.plot(data.values)

  plt.xticks(list(range(groupSize)), group)

  plt.show()



