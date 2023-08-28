#Import needed libraries for csv processing
import pandas as pd
import numpy as np


# Load BRUMEG AAL2 abs 25 csv
brumeg_aal2_abs_25 = pd.read_csv("output/convergenceBRUMEG_AAL2_abs_25.csv")

#Load the second part of the BRUMEG AAL2 abs 25 csv
brumeg_aal2_abs_25_2 = pd.read_csv("output/convergenceBRUMEG_AAL2_abs_25_part2.csv")

#To the second part, add 25 to every value in the NG Sim column
brumeg_aal2_abs_25_2['NG sim'] = brumeg_aal2_abs_25_2['NG sim'] + 25

#Merge the two dataframes
brumeg_aal2_abs_25 = pd.concat([brumeg_aal2_abs_25, brumeg_aal2_abs_25_2])

#Sort the dataframe by subject
# brumeg_aal2_abs_25.sort_values('Subject', inplace=True)

#Reset the index of the dataframe
brumeg_aal2_abs_25.reset_index(inplace=True, drop=True)

#Remove the Unmamed: 0 column
brumeg_aal2_abs_25.drop('Unnamed: 0', axis=1, inplace=True)

#Print the dataframe
print(brumeg_aal2_abs_25)

#Export to csv
brumeg_aal2_abs_25.to_csv("output/convergenceBRUMEG_AAL2_abs_50.csv", index=False)