#!/usr/bin/env python


''' This file has the abstract class for language model creation and evaluation
TODO: add model persistence and loading.
'''

class SmoothedModel:
  def __init__(self):
    ''' store the model tuple here
    '''
    self.has_model = False # change to True when the model has been generated.
    pass

  def generate_model(self, train):
    ''' override this method to generate a model.  
    The model is a tuple whose contents depend onthe type of 
    smoothing to be performed.
    '''
    self.has_model = True
    pass

  def evaluate(self, test):
    ''' Given a tokenized test sentence, use the model
    to evaluate its smoothed probability.
    Return the calculated probability
    '''
    if not self.has_model:
      return 0.0
    pass

