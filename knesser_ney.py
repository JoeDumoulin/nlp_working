#!/usr/bin/env python

from model_smoothing import SmoothedModel
from word_counts import CondFreqs, AccumCondFreqs
from ngram_helpers import generate_ngrams
from math import log
from operator import add
from itertools import islice

class KnesserNey(SmoothedModel):
  def __init__(self, n=2):
    """Initialize your data structures in the constructor."""
    self.kn_ngram_prob = {}
    self.discount = 0.75
    self.full_discount = 0.0
    self.continuation_prob = {}
    self.n = n  #bigrams?  trigrams? other?
    SmoothedModel.__init__(self)

  def generate_model(self, train):
    every_word = set()
    self.freq = {}
    condFreq = {}
    continuation = {}
    # get ngrams
    for sent in train:
      condFreq = AccumCondFreqs(condFreq, CondFreqs(generate_ngrams, [w for w in sent], self.n))
    # count the number of times each prefix starts an ngram
    for p, s in condFreq.iteritems():
      if p not in self.freq:
        self.freq[p] = {}
      self.freq[p] = len(s.items())
      # continuation probability counts
      for w,c in s.iteritems():
        if w not in continuation:
          continuation[w] = set()
        continuation[w].add(p)
    # now calculate the model parameters
    unique_ngram_starts = float(len(condFreq))
    self.full_discount = log(self.discount/reduce(add, self.freq.values()))
    for p, s in condFreq.iteritems():
      self.kn_ngram_prob[p] = {}
      interpolation_weight = self.discount*(float(len(s)))/self.freq[p]
      for w,c in s.iteritems():
        initial_term_count = float(len(continuation[w]))
        self.kn_ngram_prob[p][w] = log(max(c - self.discount, 0.0)/self.freq[p] + \
          (interpolation_weight * initial_term_count)/unique_ngram_starts) 
    SmoothedModel.generate_model(self, train)
    
  def evaluate(self, sentence):
    score = 0.0
    for i in range (len(sentence)-1):
      bigram = [bi_term for bi_term in islice(sentence, i, i+2)]
      score += self.score_term(bigram)
    return score
    
  def score_term(self, bigram):
    t1, t2 = bigram
    if t1 in self.kn_ngram_prob:
      if t2 in self.kn_ngram_prob[t1]:
        return self.kn_ngram_prob[t1][t2]
      else:
        return log(self.discount/self.freq[t1])
    else:
      return self.full_discount
      
