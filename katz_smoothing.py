#!/usr/bin/env python

from model_smoothing import SmoothedModel
from word_counts import CondFreqs, AccumCondFreqs
from ngram_helpers import generate_ngrams
from good_turing import *
from math import log

class KatzSmoothing(SmoothedModel):
  def __init__(self, n=3):
    '''initialize with the ngram arity for the model we are building
    '''
    self.n = n  #bigrams?  trigrams? other?
    self.model = () # a tuple to store the model
    self.k = 5
    SmoothedModel.__init__(self)

  def __d(r_star, r, k, n_k, n_k1):
    ''' given the gt count, actual count of ngrams, 
    limit k, and the frequency of frequency for ngrams 
    with count 1 and k+1, return the smoothing factor d 
    for ngrams with count less than k.
    '''
    factor = (k+1)*n_k1/n_1
    numerator = r_star/r - factor
    denominator = 1 - factor
    return numerator/denominator

  def find_n_k(freq_parameters):
    for p,s in freq_parameters.iteritems():
      for w,c in s.iteritems():
        r_start, nr, nr1, r = c
        

  def __model_probs(freq_parameters):
    freqs, N = freq_parameters
    probs = {}
    single_count_prob = 1.0
    for p,s in freqs.iteritems():
      if p not in probs:
        probs[p] = {}
      for w,c in s.iteritems():
        r_start, nr, nr1, r = c
        c_katz = r
        if r <= k:
          if r > 0.0:
            c_katz = self.__d(r_star, self.k, 
        probs[p][w] = r/N
        if probs[p][w] < single_count_prob:
          single_count_prob = probs[p][w]
    return (probs, single_count_prob)
  
    pass

  def generate_model(self, train):
    ''' given a list of lists of tokenized sentences, generate and store 
    a model corresponding to this type of smoothing.
    >>>
    '''
    cacc = {}
    for line in train:
      cacc = AccumCondFreqs(cacc, CondFreqs(generate_ngrams, [t for t in line], self.n))
    fof = [(i, float(len(n))) for (i,n) in freqOfFreq(cacc)]
    probs = self.__model_probs(smoothed_counts(cacc, linear_regression(fof, log)))
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

