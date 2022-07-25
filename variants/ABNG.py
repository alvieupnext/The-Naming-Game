from variants.BaselineNG import *

class ABNG(BaselineNG):
  def invent(self, topic, agent):
    flipBit = random.randint(0, 1)
    name = ''
    if flipBit:
      name = 'A'
    else: name = 'B'
    self.adopt(name, topic, agent, agent)
    return name