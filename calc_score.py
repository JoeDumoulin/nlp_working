#!/usr/bin/env python

from load_att_file import readchats
from ngram_helpers import preprocess, tokenize
from additive_smoothing import AdditiveSmoothing
from evaluation import cross_entropy

if __name__ == '__main__':
  #partition the data
  data = [[w for w in tokenize(preprocess(line[line.find(' ')+1:]))] for line in readchats('out.txt')]
  train = data[:10000]
  test = data[-10000:]

  a_s = AdditiveSmoothing()
  #generate and test some models
  a_s.generate_model(train[:100])
  print cross_entropy(a_s, test[:10000])

  a_s.generate_model(train[:1000])
  print cross_entropy(a_s, test[:10000])

  a_s.generate_model(train[:10000])
  print cross_entropy(a_s, test[:10000])

