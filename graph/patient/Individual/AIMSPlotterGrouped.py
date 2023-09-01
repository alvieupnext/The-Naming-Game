import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from patients.patientData import *

#Load the functional csv_results
convergence = hcp_convergence

#Load the behavioral csv_results
behavioral = hcp_behavioral_data

#Merge the convergence with the patient data to get
convergence = convergence.merge(behavioral, on='Subject')

first_group = lowest_hcp_patients

second_group = highest_hcp_patients

first_group_label = 'Lowest Processing Speed'

second_group_label = 'Highest Processing Speed'

consensus_levels = ['SC_0.7', 'SC_0.8', 'SC_0.9', 'SC_0.95', 'SC_0.98', 'SC_1']

percentage_titles = ['70%', '80%', '90%', '95%', '98%', '100%']


def histogram(df):
    consensus_columns = [col for col in df.columns if col.startswith('SC_')]
    plt.figure(figsize=(15, 8))
    sns.boxplot(data=df[consensus_columns])
    plt.title('Distribution of Consensus Iterations for Different Consensus Levels (HCP)')
    plt.xlabel('Consensus Level')
    plt.ylabel('Consensus Iterations')
    plt.xticks(rotation=45)
    plt.show()

def scatterplot(df, attribute='SDMT', name='SDMT'):
    df = df.dropna(subset=[attribute])
    # Function to create subplot with regression line and Pearson correlation
    def create_subplot(ax, x, y, xlabel, ylabel, title, group):
        sns.scatterplot(x=x, y=y, ax=ax, hue=group, palette=['blue', 'red'], alpha=0.5)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        # Calculate Pearson correlation for each group
        mask_low = group == first_group_label
        mask_high = group == second_group_label
        r_low, p_low = stats.pearsonr(x[mask_low], y[mask_low])
        r_high, p_high = stats.pearsonr(x[mask_high], y[mask_high])
        ax.annotate(f"{first_group_label}:\n r = {r_low:.2f}\np = {p_low:.2f}", xy=(0.05, 0.9), xycoords='axes fraction')
        ax.annotate(f"{second_group_label}:\n r = {r_high:.2f}\np = {p_high:.2f}", xy=(0.05, 0.7), xycoords='axes fraction')

    # Create a new column to differentiate between the two groups based on 'Subject' column
    df['Group'] = np.where(df['Subject'].isin(first_group), first_group_label, second_group_label)

    # Create subplots for each consensus level
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    for ax, consensus in zip(axes.ravel(), consensus_levels):
        create_subplot(ax, df[attribute], df[consensus], xlabel=f'{attribute} Score',
                       ylabel=f'{consensus[3:]} Consensus Iterations',
                       title=f'Relationship Between {name} Score and {consensus[3:]} Consensus Iterations',
                       group=df['Group'])

    plt.tight_layout()
    plt.show()

def cdf(df):
    # Function to create CDF subplot with percentage titles
    def create_cdf_subplot(ax, data_low, data_high, title):
        sns.ecdfplot(data=data_low, ax=ax, label=first_group_label, color='blue')
        sns.ecdfplot(data=data_high, ax=ax, label=second_group_label, color='red')
        ax.set_xlabel('Consensus Iterations')
        ax.set_ylabel('Cumulative Probability')
        ax.set_title(title)
        ax.legend()

    # Create a new column to differentiate between the two groups based on 'Subject' column
    df['Group'] = np.where(df['Subject'].isin(first_group), first_group_label, second_group_label)

    # Create subplots for each consensus level with percentage titles and a main title
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Cumulative Distribution Functions (CDFs) of Consensus Iterations', fontsize=16)

    for ax, (consensus, pct_title) in zip(axes.ravel(), zip(consensus_levels, percentage_titles)):
        data_low = df[df['Group'] == first_group_label][consensus]
        data_high = df[df['Group'] == second_group_label][consensus]
        create_cdf_subplot(ax, data_low, data_high, title=f'{pct_title} Consensus')

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to fit main title
    plt.show()

# Now you can simply call the function to plot
cdf(convergence)



def distribution(df):
    # Function to create histogram subplot
    def create_histogram_subplot(ax, data, title):
        sns.histplot(data=data, kde=True, ax=ax)
        ax.set_xlabel('Consensus Iterations')
        ax.set_title(title)

    # Create subplots for each consensus level with percentage titles and a main title
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Distribution of Consensus Iterations for Different Consensus Levels', fontsize=16)

    for ax, (consensus, pct_title) in zip(axes.ravel(), zip(consensus_levels, percentage_titles)):
        create_histogram_subplot(ax, df[consensus], title=f'{pct_title} Consensus')

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to fit main title
    plt.show()


def t_test(df, attribute='Subject'):
    from scipy.stats import ttest_ind

    # Divide subjects into the specified two groups
    group_low = df[df[attribute].isin(first_group)]
    group_high = df[df[attribute].isin(second_group)]

    # Perform two-sample t-tests for each consensus level and store the results
    ttest_results = []
    for consensus, pct_title in zip(consensus_levels, percentage_titles):
        t_stat, p_value = ttest_ind(group_low[consensus], group_high[consensus])
        ttest_results.append((pct_title, t_stat, p_value))

    # Display t-test results
    ttest_results_df = pd.DataFrame(ttest_results, columns=['Consensus Level', 'T-Statistic', 'P-Value'])
    print(ttest_results_df)


# Function to create a time series plot for given consensus levels
def create_timeseries(data, consensus_levels, percentage_titles, title):
    # Calculating means for each consensus level
    mean_values_first = [data[data['Subject'].isin(first_group)][level].mean() for level in consensus_levels]
    mean_values_second = [data[data['Subject'].isin(second_group)][level].mean() for level in consensus_levels]

    plt.figure(figsize=(12, 6))
    plt.plot(percentage_titles, mean_values_first, marker='o', label='First Group')
    plt.plot(percentage_titles, mean_values_second, marker='o', label='Second Group')
    plt.title(title, fontsize=16)
    plt.xlabel('Consensus Level')
    plt.ylabel('Mean Consensus Iterations')
    plt.legend()
    plt.grid(True)
    plt.show()



# Create time series plot for the updated data
create_timeseries(convergence, consensus_levels, percentage_titles,
                  'Time Series of Mean Consensus Iterations for Different Levels')

# histogram(convergence)

# scatterplot(convergence, 'PMAT24_A_CR', 'Raven')

# cdf(convergence)

# distribution(convergence)

# t_test(convergence)

# fourQuartilesCDF(convergence)

# fourQuartilesHistogram(data)