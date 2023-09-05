import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from patients.patientData import *

#Load the functional csv_results
convergence = brumeg_functional_convergence

#Load the behavioral csv_results
behavioral = brumeg_functional_data

#Merge the convergence with the patient data to get
convergence = convergence.merge(behavioral, on='Subject')

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

def scatterplot(df, attribute='SDMT'):
    # Function to create subplot with regression line and Pearson correlation
    def create_subplot(ax, x, y, xlabel, ylabel, title):
        sns.regplot(x=x, y=y, ax=ax, scatter_kws={'s': 10})
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        r, p = stats.pearsonr(x, y)
        ax.annotate(f"r = {r:.2f}\np = {p:.2f}", xy=(0.05, 0.9), xycoords='axes fraction')

    # Create subplots for each consensus level
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    for ax, consensus in zip(axes.ravel(), consensus_levels):
        create_subplot(ax, df[attribute], df[consensus],
                       xlabel=f'{attribute} Score', ylabel=f'{consensus[3:]} Consensus Iterations',
                       title=f'Relationship Between {attribute} Score and {consensus[3:]} Consensus Iterations (HCP)')

    plt.tight_layout()
    plt.show()

def cdf(df):
    # Function to create CDF subplot with percentage titles
    def create_cdf_subplot(ax, data, title):
        sns.ecdfplot(data=data, ax=ax)
        ax.set_xlabel('Consensus Iterations')
        ax.set_ylabel('Cumulative Probability')
        ax.set_title(title)

    # Create subplots for each consensus level with percentage titles and a main title
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Cumulative Distribution Functions (CDFs) of Consensus Iterations', fontsize=16)

    for ax, (consensus, pct_title) in zip(axes.ravel(), zip(consensus_levels, percentage_titles)):
        create_cdf_subplot(ax, df[consensus], title=f'{pct_title} Consensus')

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to fit main title
    plt.show()


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

def t_test(df, attribute='SDMT'):
    from scipy.stats import ttest_ind
    # Divide subjects into two groups based on median attribute score
    median_sdmt = df[attribute].median()
    group_low = df[df[attribute] <= median_sdmt]
    group_high = df[df[attribute] > median_sdmt]

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
    mean_values_low = [data[data['SDMT'] <= data['SDMT'].median()][level].mean() for level in consensus_levels]
    mean_values_high = [data[data['SDMT'] > data['SDMT'].median()][level].mean() for level in consensus_levels]

    plt.figure(figsize=(12, 6))
    plt.plot(percentage_titles, mean_values_low, marker='o', label='Low SDMT Group')
    plt.plot(percentage_titles, mean_values_high, marker='o', label='High SDMT Group')
    plt.title(title, fontsize=16)
    plt.xlabel('Consensus Level')
    plt.ylabel('Mean Consensus Iterations')
    plt.legend()
    plt.grid(True)
    plt.show()

def fourQuartilesCDF(df):

    # Divide the SDMT scores into quartiles
    df['SDMT_Quartile'] = pd.qcut(df['SDMT'], q=4, labels=["Q1", "Q2", "Q3", "Q4"])

    # Plotting CDFs for each consensus level in separate subplots
    fig, axes = plt.subplots(3, 2, figsize=(15, 12), sharex=True, sharey=True)
    consensus_levels = ["SC_0.7", "SC_0.8", "SC_0.9", "SC_0.95", "SC_0.98", "SC_1"]
    colors = ["blue", "orange", "green", "red"]
    labels = ["Q1 (Lowest)", "Q2", "Q3", "Q4 (Highest)"]

    for ax, level in zip(axes.ravel(), consensus_levels):
        for group, color, label in zip(df["SDMT_Quartile"].cat.categories, colors, labels):
            sns.ecdfplot(data=df[df["SDMT_Quartile"] == group], x=level, ax=ax, label=label,
                         color=color)
        ax.set_title(f"{int(float(level.split('_')[1]) * 100)}% Consensus")
        ax.set_xlabel("Consensus Iterations")
        ax.legend()

    fig.suptitle("CDF of Consensus Iterations by SDMT Quartiles", fontsize=16, y=0.98)
    fig.tight_layout()

    plt.show()

def fourQuartilesHistogram(df):
    # Defining the quartile groups for the SDMT scores
    df['SDMT_quartile'] = pd.qcut(df['SDMT'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

    quartile_groups = ['Q1', 'Q2', 'Q3', 'Q4']
    colors = ['red', 'blue', 'green', 'purple']

    # Creating the histograms with separate colors
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharex=True, sharey=True)

    for ax, level in zip(axes.ravel(), consensus_levels):
        for idx, quartile in enumerate(quartile_groups):
            sns.histplot(df[df['SDMT_quartile'] == quartile][level], ax=ax, kde=False,
                         bins=50, color=colors[idx], label=f"Q{idx + 1}")
            ax.set_title(f"Distribution at {float(level.split('_')[1]) * 100:.0f}% Consensus")
            ax.legend()

    plt.tight_layout()
    fig.subplots_adjust(top=0.91)  # Adjust this value to increase/decrease whitespace at the top
    fig.suptitle('Distribution of Consensus Iterations by SDMT Quartile for Different Consensus Levels', fontsize=16)
    plt.show()



# Create time series plot for the updated data
# create_timeseries(data, consensus_levels, percentage_titles,
#                   'Time Series of Mean Consensus Iterations for Different Levels')

# histogram(convergence)

scatterplot(convergence, 'SDMT')

# cdf(convergence)

# distribution(convergence)

# t_test(convergence)

# fourQuartilesCDF(convergence)

# fourQuartilesHistogram(convergence)