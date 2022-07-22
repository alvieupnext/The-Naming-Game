from variants.BaselineNG import *
#according to the paper document (The Naming Game)
#remove procedure could be moved into its own class (if desired)
class Imitation(BaselineNG):
  #Code for removing a topic from Agent memory
  def remove(self, topic, agent):
    for pairName, pairTopic in self.memory[agent]:
      #if name of pair corresponds with the adopted name
      if pairTopic == topic:
        self.memory[agent].remove((pairName, topic))
        self.display(f"Removed this pair from Agent memory {agent}: {pairName}, {pairTopic}")

  def adopt(self, name, topic, listener, speaker):
    #remove all previous bindings of the topic with the name
    self.remove(topic, listener)
    # if succesfull, run super
    super().adopt(name, topic, listener, speaker)

#according to Guy Nagels, only success should clear memory
class Imitationv2(BaselineNG):
  #Code for removing a topic from Agent memory, preserving the original binding
  def remove(self, topic, agent, name):
    for pairName, pairTopic in self.memory[agent]:
      #if name of pair corresponds with the adopted name
      if pairTopic == topic and name != pairName:
        self.memory[agent].remove((pairName, topic))
        self.display(f"Removed this pair from Agent memory {agent}: {pairName}, {pairTopic}")
  #same code but only performs clear on success
  def success(self, speaker, listener, topic, name):
    #remove all previous bindings of the topic from both speaker and listener memory
    self.remove(topic, speaker, name)
    self.remove(topic, listener, name)
    #invoke super
    super().success(speaker, listener, topic, name)
