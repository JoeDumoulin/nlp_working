#!/usr/bin/env python

from math import log

def log_prob(model, sent):
  return log(model.evaluate(sent), 2.0)

def cross_entropy(model, sents):
  ''' given a language model, an evaluation 
  method,  and a list of tokenized sentences, 
  return the cross-entropy of the sentence 
  in that model.
  '''
  W_T = 0.0
  e = 0.0
  for sent in sents:
    W_T += float(len(sent))
    e += model.evaluate(sent)
  if W_T is 0.0:
    print 'zero word total?'
    print 'W_T = %f' %W_T
    print 'e = %f' %e
    return 0
  return -1.0/W_T * e

