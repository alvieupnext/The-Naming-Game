# Import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns

#Import from patients folder brumeg_aal2_functional from the loadBrumegData.py file
from patients.patientData import brumeg_functional_convergence

merged_data = brumeg_functional_convergence

# Create box plots for different consensus levels
consensus_columns = [col for col in merged_data.columns if col.startswith('SC_')]
plt.figure(figsize=(15, 8))
sns.boxplot(data=merged_data[consensus_columns])
plt.title('Distribution of Consensus Iterations for Different Consensus Levels')
plt.xlabel('Consensus Level')
plt.ylabel('Consensus Iterations')
plt.xticks(rotation=45)
plt.show()
