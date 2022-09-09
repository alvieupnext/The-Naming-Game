import bct
from patientData import *
from matplotlib import pyplot as plt

array = loadHPCData("netmats2")

patientNames = array

character_path_lengths = []


for patient in patientNames:
  character_path_length = bct.charpath(patient)
  character_path_lengths.append(character_path_length[1])

# plt.title("Character Path Lengths")
plt.title("Global Efficiency")

plt.xlim(0, 30)


plt.hist(character_path_lengths, bins=1000)

plt.show()



