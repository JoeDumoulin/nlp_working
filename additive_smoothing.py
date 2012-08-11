#!/usr/bin/env python

from model_smoothing import SmoothedModel
from word_counts import CondFreqs, AccumCondFreqs
from ngram_helpers import generate_ngrams

class AdditiveSmoothing(SmoothedModel):
  def __init__(self, n=3):
    '''initialize with the ngram arity for the model we are building
    '''
    self.n = n  #bigrams?  trigrams? other?
    self.model = () # a tuple to store the model
    SmoothedModel.__init__(self)

  def __single_vocab(self, freq):
    return [w for w,c in freq.iteritems()]
  
  def __vocab(self, cond_freq):
    '''
    return a tuple of the number of vocab terms and a list of 
    vocab terms.  vocab is based on the conditional terms only.
    In the case of ngram terms, this means that the first terms 
    will be ignored (e.g, when counting c(b|a), we only count b).
    One consequence of this is that <s> markers aren't counted 
    in ngram counts.
    '''
    v = set()
    for i,f in cond_freq.iteritems():
      v = v | set(self.__single_vocab(f))
    return float(len(v)), v
  
  def __smoothed_probs(self, cond_freqs,delta=1.0):
    ''' each individual count will have one added to it and
    the total counts will have V added to it, where V is the 
    sum of the 1's added. 
    '''
    V,words=self.__vocab(cond_freqs)
    probs = {}
    for prefix,freqs in cond_freqs.iteritems():
      probs[prefix] = {}
      N = float(len(freqs))
      for term,count in freqs.iteritems():
        probs[prefix][term] = float(count+delta)/(delta*V+N)
    return probs,V

  def generate_model(self, train):
    ''' given a list of lists of tokenized sentences, generate and store 
    a model corresponding to this type of smoothing.
    '''
    cacc = {}
    for line in train:
      cacc = AccumCondFreqs(cacc, CondFreqs(generate_ngrams, [t for t in line], self.n))
    self.model = self.__smoothed_probs(cacc)
    SmoothedModel.generate_model(self, train)
  
  def evaluate(self, sentence):
    ''' evaluate a tokenized sentence probability using the passed-in
    ngram model
    '''
    SmoothedModel.evaluate(self, sentence)
    probs,V = self.model
    p = 1.0
    cf =  CondFreqs(generate_ngrams, sentence, self.n)
    for prefix,suffix in cf.iteritems():
      if prefix not in probs:
        p *= 1.0/(1.0+V)
      else:
        for term,count in suffix.iteritems():
          N = len(probs[prefix])
          if term in probs[prefix]:
            p *= count * probs[prefix][term]
          else:
            p *= count * (1.0/(V+N))
    return p

