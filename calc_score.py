#!/usr/bin/env python

from load_att_file import readchats
from ngram_helpers import preprocess, tokenize, generate_ngrams
from word_counts import CondFreqs, AccumCondFreqs
from additive_smoothing import AdditiveSmoothing
from evaluation import cross_entropy

if __name__ == '__main__':
  #partition the data
  data = [[w for w in tokenize(preprocess(line[line.find(' ')+1:]))] for line in readchats('out.txt')]
  train = data[:10000]
  test = data[-10000:]

  # create a trigram model
  a_s = AdditiveSmoothing()
  a_s.generate_model(train)

  # test the trigram model
  #compute cross entropy for these sentences
  print cross_entropy(a_s, test[:10])
  print cross_entropy(a_s, test[:100])
  print cross_entropy(a_s, test[:1000])
  print cross_entropy(a_s, test[:10000])

