import numpy as np
import gensim


#create the game environment to wrap the game
class environment():
  def __init__(self):
    modelPath="D:\\projectContexto\\contextoApp\\GoogleNews-vectors-negative300.bin"
    wordsPath= "D:\\projectContexto\\contextoApp\\nouns.txt"

    #create our model
    self.model= gensim.models.keyedvectors.Word2VecKeyedVectors.load_word2vec_format(modelPath, binary=True)
    #get the words that our model can recognize
    self.vocabs= list(self.model.key_to_index.keys())
    self.observation=  dict()
    self.reward=0
    self.done= False
    self.action= " "
    #get the avilabe words which are the most common words in english
    self.action_space= [line.strip() for line in open(wordsPath, 'r')]
    self.target_word=np.random.choice(self.action_space)
    self.attempts= 0
    self.distances=dict()
  
  def reset(self):
    self.target_word=np.random.choice(self.action_space)
    self.observation=  dict()
    self.reward=0
    self.done= False
    self.action= " "
    self.attempts= 0
    self.distances=dict()
    return self.observation, self.reward, self.done


  def act(self, action):
    if not self.done:
      if action not in self.action_space:
        print("word not in avilable words")
        self.reward= -1000
        self.observation[action]= self.reward 
        self.attempts+= 1
        return self.observation, self.reward, self.done
      else:
        similarity= self.model.similarity(action, self.target_word)
        self.reward= similarity
        self.observation[action]= similarity
        if (similarity>= 0.999):
          self.done= True
        return self.observation, self.reward, self.done
    else:
      self.observation, self.reward, self.done= self.reset()
      return self.observation, self.reward, self.done

  def as_len(self):
      return len(self.action_space)
  
  def play(self, value):
    while not self.done:
      #val = input("Enter your guess: ")
      self.observation, self.reward, self.done =self.act(value)
      return self.observation, self.reward, self.done
    
  def get_most_similar_words(self):
    for w in self.action_space:
      if w in self.vocabs:
        self.distances[w]= self.model.distance(w, self.target_word)
      #get most similar words
      self.most_similar= sorted(self.distances.items(), key= lambda x:x[1])
      return self.most_similar #sorted dict with most similar words
    
  #returnes the target word after you giveup
  def giveup(self):
    return self.target_word

