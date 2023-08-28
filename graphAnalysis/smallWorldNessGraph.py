import bct
from patients.patientData import *
from smallWorldNess import *
from matplotlib import pyplot as plt

array = loadHPCData("netmats2")

patientNames = array

smallWorldNesses = []


for patient in patientNames:
  clustering_coef = bct.clustering_coef_wu(patient)
  meanCluster = np.mean(clustering_coef)
  characteristic_path_length = bct.charpath(patient)
  smallWorld = smallWorldNess(meanCluster, characteristic_path_length[0])
  smallWorldNesses.append(smallWorld)

# plt.title("Character Path Lengths")
plt.title("SmallWorldNess")


plt.hist(smallWorldNesses)

plt.show()