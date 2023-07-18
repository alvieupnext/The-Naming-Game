from patientData import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

population = loadHPCData("netmats2")

print(population[0].shape)

#Subjects are a txt file seperated by newlines so we need to process the txt and add the subjects to a list
#Keep in mind that patients/subjects.txt is from the root of the project, not of the current directory

subjectsStream = open("subjects.txt", "r")

subjects = subjectsStream.read().split("\n")

#Remove the last element of the list because it is an empty string
subjects.pop()

#Subjects are strings to convert them to integers
subjects = [int(subject) for subject in subjects]



for index,patient in enumerate(subjects[25:41]):
  data = population[index]
  mask = np.zeros_like(data)
  mask[np.triu_indices_from(mask)] = True
  plt.subplot(4, 4, index + 1)
  with sns.axes_style("white"):
    ax = sns.heatmap(data, mask=mask,  square=True,  cmap="YlGnBu")
    ax.set_title(patient, x=0.8, y=0.5)

plt.show()