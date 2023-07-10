import bct
from patientData import *
from matplotlib import pyplot as plt

array = loadHPCData("netmats2")

patientNames = array

clustering_coefs = []


for patient in patientNames:
 # clustering_coef = bct.clustering_coef_wu(patient)
  clustering_coef = bct.transitivity_wu(patient)
  clustering_coefs.append(np.mean(clustering_coef))

# plt.title("Character Path Lengths")
# plt.title("Clustering Coefficient")
plt.title("Transivity")

# plt.xlim(0, 30)

plt.hist(clustering_coefs, bins=10)

print(len(clustering_coefs))

plt.show()



