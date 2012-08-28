#!/usr/bin/env python

from math import log,exp
from operator import itemgetter, mul
from ngram_helpers import generate_ngrams
from word_counts import Freqs, AccumFreqs, CondFreqs, AccumCondFreqs

def bigram_freqs(train):
  ''' given a list of tokenized sentences, return 
  bigram frequencies for this model
  >>> from nltk.data import load
  >>> sent_seperator = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_seperator.tokenize(g.raw('carroll-alice.txt'))
  >>> from ngram_helpers import preprocess, tokenize
  >>> data_gen = [tokenize(preprocess(sent)) for sent in sents]
  >>> bigram_freqs(data_gen).items()[:5]
  [('secondly', {'because': 2.0}), ('pardon', {'said': 1.0, '</s>': 4.0, 'your': 1.0}), ('saves', {'a': 1.0}), ('knelt', {'down': 1.0}), ('four', {'feet': 1.0, 'hours': 2.0, 'thousand': 1.0, 'inches': 1.0, 'times': 3.0})]
  >>>
  '''
  cond_freqs = {}
  for sent in train:
    cond_freqs = AccumCondFreqs(cond_freqs, CondFreqs(generate_ngrams, sent, 2))
  return cond_freqs

def freqOfFreq(freq):
  ''' given a dictionary of ngrams, re-index the ngrams by thier
  frequency.
  >>> from nltk.data import load
  >>> sent_seperator = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_seperator.tokenize(g.raw('carroll-alice.txt'))
  >>> from ngram_helpers import preprocess, tokenize
  >>> data_gen = [tokenize(preprocess(sent)) for sent in sents]
  >>> freqOfFreq(bigram_freqs(data_gen))[30:35]
  [(33.0, [('that', 'she'), ('and', 'then'), ('she', 'could')]), (32.0, [('<s>', 'what')]), (31.0, [('was', 'a'), ('march', 'hare')]), (30.0, [('the', 'march'), ('the', 'other'), ('could', 'not')]), (29.0, [('<s>', 'there'), ('<s>', 'but'), ('can', 'not'), ('so', 'she'), ('again', '</s>'), ('she', 'went')])]
  >>> 
  '''
  fof = {}
  for p,s in freq.iteritems():
    for w,f in s.iteritems():
      if f not in fof:
        fof[f] = []
      fof[f].append((p,w))
  return sorted(fof.items(), key=itemgetter(0), reverse=True)

''' Good-Turing smoothing requires a method for smoothing the fof numbers.
the fof smoothing in here is supported using log-log linear regression.
see Gale-Sampson,1995.
'''

def linear_regression(list_of_tuples, fn=lambda x: x):
  ''' Given a list of tuples of floats, and a function
  return the slope and intercept of the regression line 
  of the data with the function applied to each element.
  >>> from nltk.data import load
  >>> sent_seperator = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_seperator.tokenize(g.raw('carroll-alice.txt'))
  >>> from ngram_helpers import preprocess, tokenize
  >>> data_gen = [tokenize(preprocess(sent)) for sent in sents]
  >>> f_to_fof = [(i, float(len(n))) for (i,n) in freqOfFreq(bigram_freqs(data_gen))]
  >>> linear_regression(f_to_fof)
  (0.12410288547515608, 0.97637511017792022)
  >>> linear_regression(f_to_fof, log)
  (0.33585101170630283, 0.0031407862682853744)
  >>> 
  '''
  N = 0.0
  x = 0.0
  y = 0.0
  x_2 = 0.0
  x_y = 0.0
  for (f,fof) in list_of_tuples:
    N += fof
    fn_f = fn(f)
    fn_fof = fn(fof)
    x += fn_f
    y += fn_fof
    x_2 += fn_f*fn_f
    x_y += fn_f*fn_fof
  slope = (N*x_y - x*y)/(N*x_2 - x*x)
  intercept = (y - slope*x)/N
  return (slope,intercept)

def smoothed_counts(freq, (slope, intercept)):
  ''' for each ngram in freq, determine r* = (r+1)*n_r_+_1/n_r 
  as the smoothed count of each ngram in the model, where:
  r = the freq for the ngram unsmoothed
  n_r = the number of ngrams with frequency r, subject to adjustment
  by the log regression line.
  >>> from nltk.data import load
  >>> from math import log
  >>> sent_seperator = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_seperator.tokenize(g.raw('carroll-alice.txt'))
  >>> from ngram_helpers import preprocess, tokenize
  >>> data_gen = [tokenize(preprocess(sent)) for sent in sents]
  >>> cf = bigram_freqs(data_gen)
  >>> fof = [(i, float(len(n))) for (i, n) in freqOfFreq(cf)]
  >>> smoothed_counts(cf, linear_regression(fof, log)).items()[10:15]
  [('assembled', {'on': 2.5242433700915288, 'about': 2.5242433700915288}), ('consider', {'their': 2.5242433700915288, 'my': 2.5242433700915288, 'your': 3.4376501960614041}), ('whose', {'cause': 2.5242433700915288, 'thoughts': 2.5242433700915288}), ('lory', {'and': 2.5242433700915288, '</s>': 2.5242433700915288, 'who': 2.5242433700915288, 'hastily': 2.5242433700915288, 'as': 2.5242433700915288, 'with': 2.5242433700915288, 'positively': 2.5242433700915288}), ('paris', {'and': 2.5242433700915288, 'is': 2.5242433700915288})]
  >>> 
  '''
  
  # rewrite the freq list with new values
  freq_rewrite = {}
  for p,s in freq.iteritems():
    if p not in freq_rewrite:
      freq_rewrite[p] = {}
    for w,r in s.iteritems():
      N_r = exp(intercept+slope*log(r))
      N_r1 = exp(intercept+slope*log(r+1))
      r_star = (r+1)*N_r1/N_r
      freq_rewrite[p][w] = r_star
  return freq_rewrite

def model_probs(freq_parameters):
  pass

if __name__ == '__main__':
  import doctest
  doctest.testmod()



