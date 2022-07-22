from abc import ABC, abstractmethod
import AgentPairs as ap
import numpy as np
import Strategy

#Here, we will be defining the abstract superclass for all of the strategies for the Naming game, in general all the Naming Game variants use the same skeleton

#TODO make methods private
class NamingGame(ABC):

  def __init__(self, simulations=2, iterations=50, display=False, strategy=Strategy.multi):
    self.simulations = simulations
    self.iterations = iterations
    self.displayEnabled = display
    self.strategy = strategy

  #setup the game
  def setup(self, matrixNetwork):
    #get number of agents
    numberOfAgents = len(matrixNetwork)
    #create a list filled with no. agents worth of empty lists, these will be the memory of the agents
    self.memory = [ [] for _ in range(numberOfAgents) ]
    #generate the context
    self.context = self.generateContext()
    #keep track of the amount of names generated
    self.inventedNames = 0

  #Generates the context for The Naming Game
  @abstractmethod
  def generateContext(self):
    pass

  #Name for object and topic are interchangeable, my usage is to align as closely to the Naming Game documentation
  #Looks up an object from memory (can return zero, one or multiple names)
  @abstractmethod
  def produce(self, object, agent):
    pass

  #Looks up a name from memory (can either return one object or no object)
  #Listener method
  @abstractmethod
  def interpret(self, name, agent):
    pass

  #Creates a new name for a certain topic
  #Speaker Method
  @abstractmethod
  def invent(self, topic, agent):
    #increase name count
    self.inventedNames += 1

  #Adopts a certain name for a topic
  #Speaker Method
  @abstractmethod
  def adopt(self, name, topic, listener, speaker):
    # say that the agent has adopted this new method
    self.display(f"Agent {listener} has adopted the name {name} for topic {topic} from agent {speaker}")

  #Chooses an object from the context (called the topic)
  @abstractmethod
  def pick(self, agent, context):
    pass

  #Code that runs in case of a success
  @abstractmethod
  def success(self, speaker, listener, topic, name):
    self.display(f"Agent {speaker} and Agent {listener} agreed that object {topic} has the name {name}")

  #Code that runs in case of a failure
  @abstractmethod
  def failure(self, speaker, listener, intendedTopic, perceivedTopic, name):
    self.display(f"Agent {speaker} and Agent {listener} did not agree with the name {name}. " +
                 f"Intended Topic: {intendedTopic}, Perceived Topic: {perceivedTopic}")

  #Create our own display which only prints when self.display is enabled
  def display(self, args):
    if self.displayEnabled:
      print(args)

  #Does one iteration of the Naming Game for all pairs
  def run(self, matrixNetwork):
    #get all possible agent pairs
    agentPairs = ap.AgentPairs().generate(matrixNetwork)
    #choose pairs based of strategy
    chosenPairs = self.strategy(agentPairs)
    for speaker, listener in chosenPairs:
      #speaker picks a topic from context
      intendedTopic = self.pick(speaker, self.context)
      #speaker produces a name for said topic
      name = self.produce(intendedTopic, speaker)
      #listeners interprets name and gives his own topic
      perceivedTopic = self.interpret(name, listener)
      #if we found a topic
      if perceivedTopic:
        if intendedTopic == perceivedTopic:
          self.success(speaker, listener, intendedTopic, name)
        else: self.failure(speaker, listener, intendedTopic, perceivedTopic, name)
      #if we haven't found a topic, listener should adopt it
      else: self.adopt(name, intendedTopic, listener, speaker)

  #Starts the Naming Game with the desired amount of simulations
  def start(self, matrixNetwork):
    print("Starting the Naming Game")
    print("Parameters: ")
    print("Simulations: " + str(self.simulations))
    print("Iterations: " + str(self.iterations))
    print("Memory Length: " + str(len(matrixNetwork)))
    if self.displayEnabled:
      print("Display Enabled")
    else: print("Display Disabled")
    #create a table
    nameTable = np.zeros((self.iterations, self.simulations))
    for sim in range(self.simulations):
      self.setup(matrixNetwork)
      for iteration in range(self.iterations):
        self.display("Iteration " + str(iteration))
        self.run(matrixNetwork)
        #update name table
        nameTable[iteration, sim] = self.inventedNames
      #visualize the simulation
      # display the current state and print vocabulary
      self.display("Simulation " + str(sim))
    for i in range(len(self.memory)):
      self.display("Agent " + str(i))
      self.display(self.memory[i])
    #return median
    return np.mean(nameTable, axis=1)






