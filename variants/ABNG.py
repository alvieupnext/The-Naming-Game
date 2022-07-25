from variants.BaselineNG import *
from variants.Imitation import *

class ABNG(Imitationv2):
  def generateName(self):
    flipBit = random.randint(0, 1)
    name = ''
    if flipBit:
      name = 'A'
    else:
      name = 'B'
    return name

