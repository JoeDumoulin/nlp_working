#!/usr/bin/env python

from model_smoothing import SmoothedModel
from word_counts import CondFreqs, AccumCondFreqs
from ngram_helpers import generate_ngrams
from good_turing import *
from math import log

class SimpleGoodTuring(SmoothedModel):
  def __init__(self, n=3):
    '''initialize with the ngram arity for the model we are building
    '''
    self.n = n  #bigrams?  trigrams? other?
    self.model = () # a tuple to store the model
    SmoothedModel.__init__(self)

  def generate_model(self, train):
    ''' given a list of lists of tokenized sentences, generate and store 
    a model corresponding to this type of smoothing.
    >>>
    '''
    cacc = {}
    for line in train:
      cacc = AccumCondFreqs(cacc, CondFreqs(generate_ngrams, [t for t in line], self.n))
    fof = [(i, float(len(n))) for (i,n) in freqOfFreq(cacc)]
    self.model = model_probs(smoothed_counts(cacc, linear_regression(fof, log)))
    SmoothedModel.generate_model(self, train)
  
  def evaluate(self, sentence):
    ''' evaluate a tokenized sentence probability using the passed-in
    ngram model
    '''
    SmoothedModel.evaluate(self, sentence)
    probs,V = self.model
    lp = 1.0
    cf =  CondFreqs(generate_ngrams, sentence, self.n)
    for prefix,suffix in cf.iteritems():
      if prefix not in probs:
        lp += log(V, 2)
      else:
        for term,count in suffix.iteritems():
          N = len(probs[prefix])
          if term in probs[prefix]:
            lp += count * log(probs[prefix][term], 2)
          else:
            lp += log(V, 2)
    return lp

