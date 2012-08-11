#!/usr/bin/env python

from word_counts import CondFreqs
from ngram_helpers import generate_ngrams

def single_vocab(freq):
  return [w for w,c in freq.iteritems()]

def vocab(cond_freq):
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
    v = v | set(single_vocab(f))
  return float(len(v)), v

def smoothed_probs(cond_freqs,delta=1.0):
  ''' each individual count will have one added to it and
  the total counts will have V added to it, where V is the 
  sum of the 1's added. 
  '''
  V,words=vocab(cond_freqs)
  probs = {}
  for prefix,freqs in cond_freqs.iteritems():
    probs[prefix] = {}
    N = float(len(freqs))
    for term,count in freqs.iteritems():
      probs[prefix][term] = float(count+delta)/(delta*V+N)
  return probs,V

def evaluate(n, model, sentence):
  ''' evaluate a tokenized sentence probability using the passed-in
  ngram model
  '''
  probs,V = model
  p = 1.0
  cf =  CondFreqs(generate_ngrams, sentence, n)
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

