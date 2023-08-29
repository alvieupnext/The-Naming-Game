from matplotlib import pyplot as plt
from patients.patientData import *
from fitter import Fitter
from fitter import get_common_distributions

print(get_common_distributions())

distros = get_common_distributions()

patientData = hcp_patient_data

patientNames = patientData['Subject'].tolist()

weights = []

for name in patientNames:
  weights.extend(getWeightsFromPatient(patientData, name))

plt.hist(weights, bins=100)

f = Fitter(weights, distributions=distros)
f.fit()
print(f.summary())

plt.title("Weight Distribution for all known patients (HCP from NetMats2)")
plt.xlabel("Weight")
plt.ylabel("Distribution")

plt.show()