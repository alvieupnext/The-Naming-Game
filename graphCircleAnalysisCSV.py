from matplotlib import pyplot as plt
from matplotlib.patches import Patch

from matplotlib.animation import FuncAnimation
import networkx as nx
from patients.patientData import *

def map_choices(choices):
  if len(choices) == 0:
    return 0
  elif len(choices) == 2:
    return 3
  elif choices[0] == 'A':
    return 1
  else:
    return 2

#print
def map_color(value):
  color_map = {0: 'lightgray', 1: 'blue', 2: 'yellow', 3: 'green'}
  return color_map[value]

# This is your weight threshold for different edge colors.
threshold = 0.5

# Open HCP with subject from csv output and get all the subject ids
hcp_names = pd.read_csv('csv/output/BRUMEG_AAL2_functional.csv')
hcp_names = hcp_names['Subject'].tolist()

print(len(hcp_names))


def preferredAction(actionMatrix, graph, name, high_percent=0, low_percent=0):
  def update(num):
    ax.clear()

    #print a message every 100 frame updates
    if num % 100 == 0:
      print(f'Frame {num} of {len(actionMatrix)}')

    # Compute the connection-weight product for each node
    node_weights = {n: sum(d['Weight'] for _, _, d in graph.edges(n, data=True)) for n in graph.nodes()}
    node_degrees = {n: d for n, d in graph.degree()}
    node_metrics = {n: node_degrees[n] * node_weights[n] for n in graph.nodes()}

    # Sort nodes by the computed metric and pick the top and bottom nodes by provided percentiles
    sorted_nodes = sorted(node_metrics.items(), key=lambda x: x[1], reverse=True)
    top_nodes = [n for n, _ in sorted_nodes[:int(len(sorted_nodes) * high_percent)]]
    bottom_nodes = [n for n, _ in sorted_nodes[-int(len(sorted_nodes) * low_percent):]]

    selected_nodes = top_nodes + bottom_nodes

    # Create a sub-matrix for only the selected nodes
    numberMatrix_selected = actionMatrix[num, :]

    node_colors = [map_color(val) for val in numberMatrix_selected]

    # Get positions, sizes, and colors only for the selected nodes
    pos = nx.spring_layout(graph, seed=42)
    pos_selected = {n: pos[n] for n in selected_nodes}
    node_sizes = [node_metrics[n] // 100 for n in selected_nodes]

    subgraph = graph.subgraph(selected_nodes)
    widths = [d['Weight'] for _, _, d in subgraph.edges(data=True)]
    edge_colors = [
      'black' if (n1 in top_nodes and n2 in top_nodes) or (n1 in bottom_nodes and n2 in bottom_nodes) else 'red' for
      n1, n2 in subgraph.edges()]

    nx.draw_networkx_edges(subgraph, pos=pos_selected, ax=ax, width=widths, edge_color=edge_colors, alpha=0.1)
    nx.draw_networkx_nodes(subgraph, pos=pos_selected, node_color=node_colors, ax=ax, node_size=node_sizes)

    # Calculate percentages for choices in current iteration
    choices = actionMatrix[num, :]
    counts = {'A': 0, 'B': 0, 'Both': 0, 'None': 0}
    for choice in choices:
      if choice == 0:
        counts['None'] += 1
      elif choice == 1:
        counts['A'] += 1
      elif choice == 2:
        counts['B'] += 1
      elif choice == 3:
        counts['Both'] += 1

    total = sum(counts.values())
    percentages = {key: (value / total) * 100 for key, value in counts.items()}

    ax.set_title(
      f"Patient {name} - Iteration: {num + 1} - A: {percentages['A']:.1f}%, B: {percentages['B']:.1f}%, Both: {percentages['Both']:.1f}%")
    ax.legend(handles=legend_elements, loc='lower right')

  fig, ax = plt.subplots()

  # Create legend
  legend_elements = [Patch(facecolor='lightgray', edgecolor='lightgray', label='None'),
                     Patch(facecolor='blue', edgecolor='blue', label='A'),
                     Patch(facecolor='yellow', edgecolor='yellow', label='B'),
                     Patch(facecolor='green', edgecolor='green', label='Both')]

  ani = FuncAnimation(fig, update, frames=actionMatrix.shape[0], repeat=False)

  ani.save(f'videos/agent_choices_graph_{name}.mp4', writer='ffmpeg')

#Load convergenceHCP_1sim_preferred_action.csv from csv/output folder in pandas
convergence_csv = pd.read_csv("csv/output/convergenceBRUMEG_1sim_preferred_action.csv", index_col=0)

numberOfAgents = 94

for name in hcp_names:
  print(name)
  csv = pd.read_csv(f'patients/BRUMEG/patient_{name}.csv')
  print(csv.head())
  graph = nx.from_pandas_edgelist(csv, source="Source", target="Target", edge_attr="Weight")
  print(graph.number_of_nodes())
  matrix = convertArrayToMatrix(readCSVData("BRUMEG_AAL2_functional", name), numberOfAgents)
  # Get output from convergence_csv based on the name of the patient (Subject)
  print(convergence_csv.head())
  output = convergence_csv.loc[convergence_csv['Subject'] == name]

  # Sort output by ascending iteration count
  output = output.sort_values(by=['Iteration'])

  #Drop the Subject and Iteration columns
  output = output.drop(columns=['Subject', 'Iteration'])

    # Convert the output to a matrix
  output = output.to_numpy()

  print(len(output))

  print (len(output[0]))

  preferredAction(output, graph, name)




# Load the patient_121921.csv from csv/output folder in pandas
# p121921_csv = pd.read_csv("csv/output/patient_121921.csv")
#
# # And patient_203923.csv
# p203923_csv = pd.read_csv("csv/output/patient_203923.csv")

# # Create a graph from the csvs (networkx)
# p121921 = nx.from_pandas_edgelist(p121921_csv, source="Source", target="Target", edge_attr="Weight")
# p203923 = nx.from_pandas_edgelist(p203923_csv, source="Source", target="Target", edge_attr="Weight")
#
# p121921_matrix = convertArrayToMatrix(readCSVData("HCP_with_subjects", 121921), numberOfAgents)
#
# p203923_matrix = convertArrayToMatrix(readCSVData("HCP_with_subjects", 203923), numberOfAgents)
#
# output = ab.start(p203923_matrix)["preferredAction"][0]
#
# print(output)
#
# preferredAction(ab, output, p203923)
