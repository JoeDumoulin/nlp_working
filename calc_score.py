#!/usr/bin/env python

from load_att_file import readchats
from ngram_helpers import preprocess, tokenize, generate_ngrams
from word_counts import CondFreqs, AccumCondFreqs
from additive_smoothing import smoothed_probs, evaluate
from evaluation import cross_entropy

if __name__ == '__main__':
  #partition the data
  data = [[w for w in tokenize(preprocess(line[line.find(' ')+1:]))] for line in readchats('out.txt')]
  train = data[:10000]
  test = data[-10000:]

  # create a trigram model
  cacc = {}
  for line in train:
    cacc = AccumCondFreqs(cacc, CondFreqs(generate_ngrams, 
      [t for t in line], 3))
  model = smoothed_probs(cacc)

  # test the trigram model
  #for line in test[:10]:
  #  print evaluate(3,model,line), [w for w in line]
  #compute cross entropy for these sentences
  print cross_entropy(lambda m,s: evaluate(3,m,s), model, test)

