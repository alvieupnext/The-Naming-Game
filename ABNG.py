from BaselineNG import *

class ABNG(BaselineNG):
  def invent(self, topic, agent):
    flipBit = random.randint(0, 1)
    name = ''
    if flipBit:
      name = 'A'
    else: name = 'B'
    self.memory[agent].append((name, topic))
    print("Agent " + str(agent) + " has invented the name " + name + " for topic " + str(topic))
    return name