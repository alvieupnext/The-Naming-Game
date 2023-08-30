import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter
import matplotlib.pyplot as plt
from patients.patientData import *


def plot_survival(group):
    # Load BRUMEG AAL2 abs csv_results
    # Load the BRUMEG AAL2 functional csv_results
    data = brumeg_functional_convergence

    # Merge the SDMT convergence with the patient data to get SDMT
    data = data.merge(brumeg_functional_data, on='Subject')

    data['event'] = data['SC_1'].notna().astype(int)
    data['duration'] = data['SC_1'].fillna(max(data['SC_1']))

    plt.figure(figsize=(10, 7))
    kmf = KaplanMeierFitter()

    if group == 1:
        kmf.fit(data['duration'], event_observed=data['event'])
        kmf.plot()
        plt.title('Kaplan-Meier Survival Curve')

    elif group == 2:
        median_SDMT = data['SDMT'].median()
        data['SDMT_group'] = np.where(data['SDMT'] < median_SDMT, 'low', 'high')

        for label, group_df in data.groupby('SDMT_group'):
            kmf.fit(group_df['duration'], event_observed=group_df['event'], label=f'SDMT {label}')
            kmf.plot()

        plt.title('Kaplan-Meier Survival Curve by SDMT group')

    elif group == 4:
        quantiles = data['SDMT'].quantile([0.25, 0.5, 0.75]).to_list()
        conditions = [
            data['SDMT'] < quantiles[0],
            (data['SDMT'] >= quantiles[0]) & (data['SDMT'] < quantiles[1]),
            (data['SDMT'] >= quantiles[1]) & (data['SDMT'] < quantiles[2]),
            data['SDMT'] >= quantiles[2]
        ]
        choices = ['Q1', 'Q2', 'Q3', 'Q4']
        data['SDMT_quartile'] = np.select(conditions, choices)

        for label, group_df in data.groupby('SDMT_quartile'):
            kmf.fit(group_df['duration'], event_observed=group_df['event'], label=f'SDMT {label}')
            kmf.plot()

        plt.title('Kaplan-Meier Survival Curve by SDMT quartile')

    else:
        print("Invalid group argument provided. Choose from 1, 2, or 4.")
        return

    plt.ylabel('Probability of Not Reaching 100% Consensus')
    plt.xlabel('Time (Iterations)')
    plt.legend()
    plt.show()


# Test the function
plot_survival(4)  # for instance
