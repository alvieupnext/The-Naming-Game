from variants.BaselineNG import *
#according to the paper document (The Naming Game)
class Imitation(BaselineNG):
  def adopt(self, name, topic, agent):
    #remove all previous bindings of the topic with the name
    for pairName, topic in self.memory[agent]:
      #if name of pair corresponds with the adopted name
      if pairName == name:
        self.memory[agent].remove((pairName, topic))
        self.display(f"Removed this pair from memory: {pairName}, {topic}")
    #add new binding
    self.memory[agent].append((name, topic))
    # if succesfull, run super
    super().adopt(name, topic, agent)
