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
  (0.12390705875224355, 0.9763969903604447)
  >>> linear_regression(f_to_fof, log)
  (0.3344705807030366, 0.0031418999519403803)
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
  >>> smoothed_counts(cf, linear_regression(fof, log))[0].items()[10:15]
  [('assembled', {'on': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'about': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506)}), ('consider', {'their': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'my': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'your': (3.435726624538815, 1.2648825094317506, 1.4485968381893783)}), ('whose', {'cause': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'thoughts': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506)}), ('lory', {'and': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), '</s>': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'who': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'hastily': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'as': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'with': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'positively': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506)}), ('paris', {'and': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506), 'is': (2.5218292235379955, 1.0031468408928865, 1.2648825094317506)})]
  >>> 
  '''
  
  # rewrite the freq list with new values
  freq_rewrite = {}
  N = 0.0
  for p,s in freq.iteritems():
    if p not in freq_rewrite:
      freq_rewrite[p] = {}
    for w,r in s.iteritems():
      N_r = exp(intercept+slope*log(r))
      N_r1 = exp(intercept+slope*log(r+1))
      r_star = (r+1)*N_r1/N_r
      freq_rewrite[p][w] = (r_star, N_r, N_r1, r)
      N += N_r * r_star
  return (freq_rewrite, N)

def model_probs(freq_parameters):
  ''' Given frequency modeling data, return model probability.
  >>> from nltk.data import load
  >>> from math import log
  >>> sent_seperator = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_seperator.tokenize(g.raw('carroll-alice.txt'))
  >>> from ngram_helpers import preprocess, tokenize
  >>> data_gen = [tokenize(preprocess(sent)) for sent in sents]
  >>> cf = bigram_freqs(data_gen)
  >>> fof = [(i, float(len(n))) for (i, n) in freqOfFreq(cf)]
  >>> model_probs(smoothed_counts(cf, linear_regression(fof, log)))[0].items()[10:15]
  [('hate', {'c': 3.279103308880836e-05, 'cats': 3.279103308880836e-05}), ('assembled', {'on': 3.279103308880836e-05, 'about': 3.279103308880836e-05}), ('forget', {'to': 3.279103308880836e-05, 'them': 3.279103308880836e-05}), ('whose', {'cause': 3.279103308880836e-05, 'thoughts': 3.279103308880836e-05}), ('lory', {'and': 3.279103308880836e-05, '</s>': 3.279103308880836e-05, 'who': 3.279103308880836e-05, 'hastily': 3.279103308880836e-05, 'as': 3.279103308880836e-05, 'with': 3.279103308880836e-05, 'positively': 3.279103308880836e-05})]
  '''
  freqs, N = freq_parameters
  probs = {}
  single_count_prob = 1.0
  for p,s in freqs.iteritems():
    if p not in probs:
      probs[p] = {}
    for w,c in s.iteritems():
      r_star, nr, nr1, r = c
      probs[p][w] = r/N
      if probs[p][w] < single_count_prob:
        single_count_prob = probs[p][w]
  return (probs, single_count_prob)

if __name__ == '__main__':
  import doctest
  doctest.testmod()



