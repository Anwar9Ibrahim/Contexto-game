import numpy as np
import torch
import torch.nn.functional as f
from transformers import BertModel, BertTokenizer
from time import sleep
from abc import ABC


class Analyzer(ABC):
  def __init__(
      self,
      similarity_func, 
      bert_version : str,
      available_words,
      target
      ):
      self.similarity_func = similarity_func

      self.bert_version = bert_version
      self.tokenizer = BertTokenizer.from_pretrained(bert_version)
      self.model = BertModel.from_pretrained(bert_version)
      self.model = self.model.eval()
      
      
      self.observations= dict()
      self.reward=0
      self.done= False
      self.action= " "
      self.action_space= available_words
      self.target = target
      self.new_target= None
      self.target_emb=self.get_word_emb(token=target) #np.random.choice(self.action_space)
      self.attempts= 0

  def get_word_emb(
      self, 
      token : str
      ):
      encoding = self.tokenizer(
          token, 
          padding=True, 
          return_tensors='pt'
          )

      for tokens in encoding['input_ids']:
        self.tokenizer.convert_ids_to_tokens(tokens)

      with torch.no_grad():
        embed = self.model(**encoding)[0]

      avg_embed = embed.mean(dim=1)

      return avg_embed
  
    
  
  def act (self, word):
      if not self.done:
          if word not in self.action_space:
              print("word not in avilable words")
              self.reward= -1000
              self.observations[word]= self.reward 
              self.attempts+= 1
              return self.observations, self.reward, self.done, self.new_target
          else:
              self.reward= self.get_similarity(self.get_word_emb(token= word), self.target_emb)
              self.observations[word]= self.reward
              self.attempts+= 1
              x= self.reward.item()
              if (x >= 0.99999):
                self.done= True
                self.new_target= np.random.choice(self.action_space)
              return self.observations, self.reward, self.done, self.new_target
      elif self.done:
          return self.observations, self.reward, self.done ,self.new_target  
    

    
  def get_similarity(self, embed1, embed2):
      return self.similarity_func(embed1, embed2)[0]
  
  def giveup(self):
     return self.target