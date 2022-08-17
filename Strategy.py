import random
#Various strategies for choosing which agent pairs become the speakers and listeners
#Every strategy gets a set of a list with agent pairs and a list of scores

#Multi-learning strategy: every single agent pair learns something
def multi(agentPairs):
  return agentPairs


#Mono-learning: only one randomly chosen pair gets to learn
def mono(agentPairs):
  index = random.randint(0, len(agentPairs) - 1)
  chosenPair = agentPairs[index]
  #Return pair in a list
  return [chosenPair]