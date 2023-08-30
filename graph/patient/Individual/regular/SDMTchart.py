from matplotlib import pyplot as plt
from patients.patientData import *

plt.title(f"SDMT chart")

plt.xlabel("Patients")

plt.ylabel("SDMT score")

patient_data = brumeg_functional_data

patientNames = patient_data['Subject'].tolist()
SDMT = patient_data['SDMT'].tolist()


groupSize = len(patientNames) // 5

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

for index, group in enumerate(patientGroups):
  plt.title(f"SDMT chart")

  plt.xlabel("Patients")

  plt.ylabel("SDMT score")

  data = SDMT[index*groupSize:index*groupSize + groupSize]



  print(data)

  plt.plot(data)

  plt.xticks(list(range(groupSize)), group)

  plt.show()



