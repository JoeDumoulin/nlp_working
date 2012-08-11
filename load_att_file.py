#!/usr/bin/env python

from ngram_helpers import *
from word_counts import *

def readchats(file_name):
  with open(file_name, 'r') as f:
    for line in f:
      yield line.strip()

if __name__ == '__main__':
  facc = {}
  cacc = {}
  chatlines = [c for c in readchats('out.txt')][:100]
  for line in chatlines:
    start = line.find(' ')
    chat = [t for t in tokenize(preprocess(line[start+1:]))]
    facc = AccumFreqs(facc, Freqs(generate_ngrams, chat, 1))
    cacc = AccumCondFreqs(cacc, CondFreqs(generate_ngrams, chat, 3))
  words = sorted(facc.iteritems(), key = lambda v: v[1])
  
  # do conditional frequencies
  trigram_freqs = cacc
  #print words
  #print trigram_freqs
  print TermProb(facc)
  print len(trigram_freqs)
  print len(words)

