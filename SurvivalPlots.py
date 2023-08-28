import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter
import matplotlib.pyplot as plt


def plot_survival(group):
    # Load BRUMEG AAL2 abs csv
    brumeg_aal2_functional = pd.read_csv("patients/BRUMEG_functional/BRUMEG_AAL2_functional.csv")

    brumeg_aal2_functional['event'] = brumeg_aal2_functional['SC_1'].notna().astype(int)
    brumeg_aal2_functional['duration'] = brumeg_aal2_functional['SC_1'].fillna(max(brumeg_aal2_functional['SC_1']))

    plt.figure(figsize=(10, 7))
    kmf = KaplanMeierFitter()

    if group == 1:
        kmf.fit(brumeg_aal2_functional['duration'], event_observed=brumeg_aal2_functional['event'])
        kmf.plot()
        plt.title('Kaplan-Meier Survival Curve')

    elif group == 2:
        median_SDMT = brumeg_aal2_functional['SDMT'].median()
        brumeg_aal2_functional['SDMT_group'] = np.where(brumeg_aal2_functional['SDMT'] < median_SDMT, 'low', 'high')

        for label, group_df in brumeg_aal2_functional.groupby('SDMT_group'):
            kmf.fit(group_df['duration'], event_observed=group_df['event'], label=f'SDMT {label}')
            kmf.plot()

        plt.title('Kaplan-Meier Survival Curve by SDMT group')

    elif group == 4:
        quantiles = brumeg_aal2_functional['SDMT'].quantile([0.25, 0.5, 0.75]).to_list()
        conditions = [
            brumeg_aal2_functional['SDMT'] < quantiles[0],
            (brumeg_aal2_functional['SDMT'] >= quantiles[0]) & (brumeg_aal2_functional['SDMT'] < quantiles[1]),
            (brumeg_aal2_functional['SDMT'] >= quantiles[1]) & (brumeg_aal2_functional['SDMT'] < quantiles[2]),
            brumeg_aal2_functional['SDMT'] >= quantiles[2]
        ]
        choices = ['Q1', 'Q2', 'Q3', 'Q4']
        brumeg_aal2_functional['SDMT_quartile'] = np.select(conditions, choices)

        for label, group_df in brumeg_aal2_functional.groupby('SDMT_quartile'):
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
