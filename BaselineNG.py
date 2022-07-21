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
    self.memory[agent][name] = topic
    print(self.memory)


