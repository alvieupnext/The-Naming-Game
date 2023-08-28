import bct
from patients.patientData import *
from matplotlib import pyplot as plt

array = loadHPCData("netmats2")

patientNames = array

efficiencies = []


for patient in patientNames:
  efficiency = bct.efficiency_wei(patient)
  print(efficiency)
  efficiencies.append(efficiency)

# plt.title("Character Path Lengths")
plt.title("Local Efficiency")


plt.hist(efficiencies)

plt.show()



