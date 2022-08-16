import random
#Various strategies for choosing which agent pairs become the speakers and listeners
#Every strategy gets a list of 3-member list (speaker, listener, score) and returns a 2-member list of chosen agents

def extractPair(agentPair):
  speaker = agentPair[0]
  listener = agentPair[1]
  #reconvert agent pair to int
  return [int(speaker), int(listener)]

#Multi-learning strategy: every single agent pair learns something
def multi(agentPairs):
  return list(map(extractPair, agentPairs))

#Mono-learning: only one randomly chosen pair gets to learn
def mono(agentPairs):
  index = random.randint(0, len(agentPairs) - 1)
  chosenPair = agentPairs[index]
  #Return pair in a list
  agentPairList = [chosenPair]
  return list(map(extractPair, agentPairList))