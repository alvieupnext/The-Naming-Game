from NamingGame import *
import random
class BaselineNG(NamingGame):
  def generateContext(self):
    range(10)

  def invent(self, topic, agent):
    #generate random string as name
    name = ''
    for _ in range(7):
      # Considering only upper and lowercase letters
      random_integer = random.randint(97, 97 + 26 - 1)
      flip_bit = random.randint(0, 1)
      # Convert to lowercase if the flip bit is on
      random_integer = random_integer - 32 if flip_bit == 1 else random_integer
      # Keep appending random characters using chr(x)
      name += (chr(random_integer))
    #update agent memory
    self.memory[agent].append((name, object))
    return name
    print(self.memory)

  #just pick a random object
  def pick(self, agent, context):
    #pick a random object from context
    index = random.randint(0, len(context) - 1)
    return context[index]

  #generates a name for object
  def produce(self, object, agent):
    #possible name matches for the object
    results = []
    #get memory and iterate through the vocabulary
    for name, topic in self.memory[agent]:
      if topic == object:
        results.append(name)
    #if we have found a result, pick a random name from our possible names
    if results:
      index = random.randint(0, len(results) - 1)
      return name
    #else invent a new name and give this new name in return
    return self.invent(object, agent)

  #
  def interpret(self, name, agent):
    #get agent memory and iterate through vocabulary
    for vocName, topic in self.memory[agent]:
      if vocName == name:
        return topic
    #if we have not encountered this name, return None
    return None

  def adopt(self, name, topic, agent):
    #store connection in agent memory
    self.memory[agent].append((name, topic))


