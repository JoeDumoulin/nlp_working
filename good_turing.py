#!/usr/bin/env python

from ngram_helpers import generate_ngrams
from word_counts import Freqs, AccumFreqs, CondFreqs, AccumCondFreqs

def bigram_freqs(train):
  ''' given a list of tokenized sentences, return 
  bigram frequencies for this model
  '''
  cond_freqs = {}
  for sent in train:
    cond_freqs = AccumCondFreqs(cond_freqs, CondFreqs(generate_ngrams, sent, 2))
  return cond_freqs

def freqOfFreq(freq):
  ''' given a dictionary of ngrams, re-index the ngrams by thier
  frequency.
  '''
  fof = {}
  for p,s in freq.iteritems():
    for w,f in s.iteritems():
      if f not in fof:
        fof[f] = []
      fof[f].append((p,w))
  return sorted(fof, key=fof.get, reverse=True)

if __name__ == '__main__':
  from load_att_file import readchats

  data = [[w for w in tokenize(preprocess(line[line.find(' ')+1:]))] for line in readchats('out.txt')]
  print freqOfFreq(bigram_freqs(data))



