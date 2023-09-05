from matplotlib import pyplot as plt
from variants.BaselineNG import *
from variants.Imitation import *
from namingGameTools import MatrixFactory as mf
from variants.ABNG import *
import numpy as np

from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D



def map_choices(choices):
  if len(choices) == 0:
    return 0
  elif len(choices) == 2:
    return 3
  elif choices[0] == 'A':
    return 1
  else:
    return 2


def preferredAction(actionMatrix):
  fig, ax = plt.subplots()
  numberMatrix = np.zeros(actionMatrix.shape)
  for x in range(actionMatrix.shape[0]):
    for y in range(actionMatrix.shape[1]):
      numberMatrix[x, y] = map_choices(actionMatrix[x, y])
  fig, ax = plt.subplots()

  # Create a scatter plot with one point for each agent.
  scatter = ax.scatter(range(numberMatrix.shape[1]), [0] * numberMatrix.shape[1], c=numberMatrix[0, :], s=100)

  # Add text to the plot to show the current iteration
  iteration_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

  # Hide the y-ticks
  plt.yticks([])

  # Create legend
  legend_elements = [Line2D([0], [0], marker='o', color='w', label='None', markerfacecolor='purple', markersize=10),
                     Line2D([0], [0], marker='o', color='w', label='A', markerfacecolor='lightgreen', markersize=10),
                     Line2D([0], [0], marker='o', color='w', label='B', markerfacecolor='yellow', markersize=10),
                     Line2D([0], [0], marker='o', color='w', label='Both', markerfacecolor='blue', markersize=10)]
  ax.legend(handles=legend_elements, loc='lower right')

  def update(frame_number):
    # Update the colors of the points based on the choices at the current iteration
    scatter.set_array(numberMatrix[frame_number, :])

    # Update the iteration text
    iteration_text.set_text(f'Iteration: {frame_number + 1}')

  # Create the animation
  ani = FuncAnimation(fig, update, frames=numberMatrix.shape[0], interval=200)

  # Save the animation
  ani.save('agent_choices_demo_trig_generated.mp4', writer='ffmpeg')


factory = mf.MatrixFactory(triangular=True)

lattice = factory.makeLatticeMatrix(100, 5)

scaleFree = factory.makeScaleFreeMatrix(100)

smallWorld = factory.makeSmallWorldMatrix(100,5, 3)

ab = ABNG(simulations=1, maxIterations=10000, strategy=Strategy.mono, output=["preferredAction"], consensusScore=[1], display=False)

output = ab.start(smallWorld)["preferredAction"][0]

print(output)

preferredAction(output)



