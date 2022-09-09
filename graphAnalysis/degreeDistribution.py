import bct
from patientData import *
from matplotlib import pyplot as plt

array = loadHPCData("netmats2")

patientNames = array[0:30]

ncols = 5

nrows = int(np.ceil(len(patientNames) / (1.0*ncols)))

fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 10))

character_path_lengths = []


for i in range(nrows):
  for j in range(ncols):
    # print(i*ncols + j)
    patient = patientNames[i*ncols + j]
    degrees = bct.strengths_und(patient)
    character_path_length = bct.charpath(patient)
    character_path_lengths.append(character_path_length[0])
    print(character_path_length[0])
    ax = axes[i, j]
    ax.hist(degrees, bins=10, color='blue', alpha=0.5, label=f"P{i*ncols + j}")
    ax.set_xlabel('x')
    ax.set_ylabel('PDF')
    leg = ax.legend(loc='upper left')
    leg.draw_frame(False)

plt.show()



