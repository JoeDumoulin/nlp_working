#!/usr/bin/env python

from good_turing import *
from model_smoothing import SmoothedModel
from word_counts import *
from ngram_helpers import generate_ngrams
from math import log
from operator import divide

class BasicGoodTuring(SmoothedModel):
  def __init(self, n=3):
    self.n = n
    self.model = ()
    SmoothedModel.__init__(self)

  def generate_model(self, train):
    ''' given a list of lists of tokenized sentences, generate and store 
    a model corresponding to this type of smoothing.
    '''
    # get the backoff frequencies
    freq = {}
    ncf = {}
    smoothedf = {}
    for i in xrange(1,self.n+1):
      ncf[i] = {}
    for line in train:
      ncf[1] = AccumFreqs(ncf[1], Freqs(generate_ngrams, [t for t in line], 1))
      for i in xrange(2,n+1):
        #get ngram frequencies up to n
        ncf[i] = AccumCondFreqs(ncf[i], CondFreqs(generate_ngrams, [t for t in line], i))
    # get the smoothed counts for each ngram
    smoothedf[1] = (ncf[1], sum(ncf[1].values()))
    for i  xrange(2,self.n+1):
      fof = fof = [(i, float(len(n))) for (i, n) in freqOfFreq(ncf[i])]
      smoothedf[i] = smoothed_counts(smoothedf[i], linear_regression(fof, log))

    # now get the model probabilities for each ngram layer
    modelp = {}
    for i,m in smoothedf.iteritems():
      probs = {}
      if i is 1:
        for w,c in m[0].iteritems():
          probs[w] = float(c)/m[1]
      for p, s in m[0].iteritems():
        probs[p] = {}
        n = float(len(s))
        for w,c in s:
          probs[p][w] = c/n
      modelp[i] = probs
      self.model = (modelp, smoothedf)
    return self.model
    SmoothedModel.generate_model(self, train)

  def evaluate(self, test):
    nmodel = self.model[self.n][0] 
    testf = 0.0
    if n is 1:
      testf = AccumFreqs(testf, Freqs(generate_ngrams, [t for t in test], n))
    else:
      testf = AccumCondFreq(testf, CondFreqs(generate_ngrams, [t for t in test], n))
    logprob = 1.0
    for p, s in testf.iteritems:
      if p not in modelp:
        for w,c in s.iteritems():
          if w in nmodel[p]:
            logprob += c*log(nmodel[p][w])
          else:
            

