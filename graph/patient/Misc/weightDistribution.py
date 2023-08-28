from matplotlib import pyplot as plt
from patients.patientData import *
from fitter import Fitter
from fitter import get_common_distributions

print(get_common_distributions())

distros = get_common_distributions()


plt.title("Weight Distribution for all known patients")
plt.xlabel("Weight")
plt.ylabel("Distribution")

patientNames = names

weights = []

for name in patientNames:
  weights.extend(getWeightsFromPatient(name))

plt.hist(weights, bins=100)

f = Fitter(weights, distributions=distros)
f.fit()
print(f.summary())

plt.show()