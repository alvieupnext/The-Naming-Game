from variants.BaselineNG import *
#according to the paper document (The Naming Game)
class Imitation(BaselineNG):
  #Code for removing a topic from Agent memory
  def remove(self, topic, agent):
    for pairName, pairTopic in self.memory[agent]:
      #if name of pair corresponds with the adopted name
      if pairTopic == topic:
        self.memory[agent].remove((pairName, topic))
        self.display(f"Removed this pair from Agent memory {agent}: {pairName}, {pairTopic}")

  def adopt(self, name, topic, agent):
    #remove all previous bindings of the topic with the name
    self.remove(topic, agent)
    # if succesfull, run super
    super().adopt(name, topic, agent)

#according to Guy Nagels, only success should clear memory
class Imitationv2(BaselineNG):
  #same code but only performs clear on success
  def success(self, speaker, listener, topic, name):
    #remove all previous bindings of the topic from both speaker and listener memory
    self.remove(topic, speaker)
    self.remove(topic, listener)
    #adopt new binding for speaker and listener
    self.adopt(name, topic, speaker)
    self.adopt(name, topic, listener)
