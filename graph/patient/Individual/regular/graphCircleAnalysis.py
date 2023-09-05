from matplotlib import pyplot as plt
from variants.ABNG import *
from namingGameTools import Strategy
from matplotlib.patches import Patch

from matplotlib.animation import FuncAnimation
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

def map_color(value):
  color_map = {0: 'lightgray', 1: 'blue', 2: 'yellow', 3: 'green'}
  return color_map[value]

# This is your weight threshold for different edge colors.
threshold = 0.5

# Open subject from csv_results output and get all the subject ids
data = hcp_patient_data
names = data['Subject'].tolist()

numberOfAgents = hcp_agents


def preferredAction(ng, actionMatrix, graph, name, high_percent=0, low_percent=0):
  def update(num):
    ax.clear()

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
    numberMatrix_selected = numberMatrix[num, selected_nodes]

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
    choices = numberMatrix[num, :]
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
  numberMatrix = np.zeros((len(actionMatrix), len(actionMatrix[0])))
  for x in range(numberMatrix.shape[0]):
    for y in range(numberMatrix.shape[1]):
      numberMatrix[x, y] = map_choices(actionMatrix[x][y])

  # Create legend
  legend_elements = [Patch(facecolor='lightgray', edgecolor='lightgray', label='None'),
                     Patch(facecolor='blue', edgecolor='blue', label='A'),
                     Patch(facecolor='yellow', edgecolor='yellow', label='B'),
                     Patch(facecolor='green', edgecolor='green', label='Both')]

  ani = FuncAnimation(fig, update, frames=numberMatrix.shape[0], repeat=False)

  ani.save(f'videos/agent_choices_graph_{name}.mp4', writer='ffmpeg')


ab = ABNG(simulations=1, maxIterations=10, strategy=Strategy.mono, output=["preferredAction"], consensusScore=[0.95], display=False)

for name in names[0:1]:
  graph = createGraphFromSubjectNumber(name, data)
  array = readFromPandasDataframe(data, name)
  matrix = convertArrayToMatrix(array , numberOfAgents)
  output = ab.start(matrix)["preferredAction"][0]

  preferredAction(ab, output, graph, name)




# Load the patient_121921.csv_results from csv_results/output folder in pandas
# p121921_csv = pd.read_csv("csv_results/output/patient_121921.csv_results")
#
# # And patient_203923.csv_results
# p203923_csv = pd.read_csv("csv_results/output/patient_203923.csv_results")

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
