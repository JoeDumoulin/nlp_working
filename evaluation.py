#!/usr/bin/env python

from math import log

def log_prob(evaluate, model, sent):
  return log(evaluate(model, sent), 2.0)

def cross_entropy(evaluate, model, sents):
  ''' given a language model, an evaluation 
  method,  and a list of tokenized sentences, 
  return the cross-entropy of the sentence 
  in that model.
  '''
  W_T = 0.0
  e = 0.0
  for sent in sents:
    W_T += float(len(sent))
    e += log_prob(evaluate, model, sent)
  return -1.0/W_T * e

