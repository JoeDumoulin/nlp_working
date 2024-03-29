#!/usr/bin/env python

def Freqs(term_generator, doc, n):
  ''' given a method of generating terms, a list of terms (doc), 
  and a term length n, return a set of counts generated by the model
  >>> from nltk.data import load
  >>> sent_tok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_tok.tokenize(g.raw('austen-emma.txt'))
  >>> from ngram_helpers import *
  >>> Freqs(generate_ngrams, [w for w in tokenize(preprocess(sents[4]))], 2)
  {'it was': 1.0, 'intimacy of': 1.0, 'of sisters': 1.0, 'them it': 1.0, 'the intimacy': 1.0, '<s> between': 1.0, 'sisters </s>': 1.0, 'between them': 1.0, 'more the': 1.0, 'was more': 1.0}
  >>>
  '''
  freqs = {}
  for t in term_generator(doc, n):
    term = (' ').join(t)
    if term not in freqs:
      freqs[term] = 0.0
    freqs[term] += 1.0
  return freqs

def AccumFreqs(acc, freqs):
  ''' given two sets of model frequencies, return their union, 
  accumulating the frequencies of the two sets.
  >>> from nltk.data import load
  >>> stok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> from ngram_helpers import *
  >>> accum = {}
  >>> for sent in stok.tokenize(g.raw('austen-emma.txt')):
  ...   accum = AccumFreqs(accum, Freqs(generate_ngrams, tokenize(preprocess(sent)), 2))
  >>> accum.items()[:10]
  [('blessed her', 1.0), ('long understood', 2.0), ('us at', 1.0), ('counteract the', 2.0), ('privilege of', 3.0), ('baronne d', 1.0), ('important </s>', 2.0), ('extricated him', 1.0), ('disposition altogether', 1.0), ('whisper especially', 1.0)]
  >>> 
  '''
  for w,c in freqs.iteritems():
    if w not in acc:
      acc[w] = 0.0
    acc[w] += c
  return acc

def TermProb(freqs):
  ''' given a dict of model frequencies, return a
  a dict of term probabilities over the model.  The probabilities 
  are maximum likelihood.
  >>> from nltk.data import load
  >>> stok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> from ngram_helpers import *
  >>> accum = {}
  >>> for sent in stok.tokenize(g.raw('austen-emma.txt')):
  ...   accum = AccumFreqs(accum, Freqs(generate_ngrams, tokenize(preprocess(sent)), 2))
  >>> TermProb(accum).items()[:5]
  [('blessed her', 1.5523129462899721e-05), ('long understood', 3.1046258925799442e-05), ('satisfaction that', 1.5523129462899721e-05), ('counteract the', 3.1046258925799442e-05), ('privilege of', 4.6569388388699159e-05)]
  >>> 
  '''
  termprobs = {}
  N = float(len(freqs))
  for term,counts in freqs.iteritems():
    termprobs[term] = float(counts)/N
  return termprobs

def CondFreqs(term_generator, doc, n):
  ''' Similar to Freqs but for conditional probabilities.
  Given a model term generator, a list of terms, and an 
  ngram number, return a dictionary of the conditional
  counts of the final ngram term with respect to the previous 
  n-1 terms.  or example, if the term generator returns ngrams 
  and n = 3, then CondFreqs will read doc, extract trigrams, and 
  then count the third token in the trigram for every time that 
  the first two tokens appear.
  >>> from nltk.data import load
  >>> sent_tok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_tok.tokenize(g.raw('austen-emma.txt'))
  >>> from ngram_helpers import *
  >>> CondFreqs(generate_ngrams, tokenize(preprocess(sents[1])), 3).items()[:5] 
  [('and had', {'in': 1.0}), ('house from', {'a': 1.0}), ('most affectionate', {'indulgent': 1.0}), ('in consequence', {'of': 1.0}), ('a very', {'early': 1.0})]
  >>> CondFreqs(generate_ngrams, [w for w in tokenize(preprocess(sents[1]))], 3).items()[:5]
  [('and had', {'in': 1.0}), ('house from', {'a': 1.0}), ('most affectionate', {'indulgent': 1.0}), ('in consequence', {'of': 1.0}), ('a very', {'early': 1.0})]
  >>> 
  '''
  cond_freqs = {}
  for term in term_generator(doc, n):
    base_term = (' ').join(term[:-1])
    cond_term = term[-1]
    if base_term not in cond_freqs:
      cond_freqs[base_term] = {}
    if cond_term not in cond_freqs[base_term]:
      cond_freqs[base_term][cond_term] = 0.0
    cond_freqs[base_term][cond_term] += 1.0
  return cond_freqs

def AccumCondFreqs(acc, cfreqs):
  ''' given two dictionaries fo conditional frequencies, join them,
  accumulate the frequencies, and return the result.
  >>> from nltk.data import load
  >>> stok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> from ngram_helpers import *
  >>> accum = {}
  >>> for sent in stok.tokenize(g.raw('austen-emma.txt')):
  ...   accum = AccumCondFreqs(accum, CondFreqs(generate_ngrams, tokenize(preprocess(sent)), 2))
  >>> accum.items()[:2]
  [('yellow', {'and': 1.0, 'curtains': 1.0, 'pattern': 1.0}), ('four', {'and': 4.0, 'horses': 2.0, 'perfectly': 1.0, 'selves': 1.0, 'months': 1.0, 'o': 3.0, 'years': 4.0, 'hours': 3.0, 'to': 1.0, 'miles': 2.0, 'servants': 1.0, 'weeks': 3.0, 'times': 1.0, '</s>': 1.0, 'children': 2.0})]
  >>> 
  '''
  for p,s in cfreqs.iteritems():
    if p not in acc:
      acc[p] = {}
    for w,c in s.iteritems():
      if w not in acc[p]:
        acc[p][w] = 0.0
      acc[p][w] += c
  return acc

def NgramProbs(cond_freqs):
  ''' given a dictionary of conditional frequencies return a
  dictionary of conditional probabilities.
  >>> from nltk.data import load
  >>> stok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> from ngram_helpers import *
  >>> accum = {}
  >>> for sent in stok.tokenize(g.raw('austen-emma.txt')):
  ...   accum = AccumCondFreqs(accum, CondFreqs(generate_ngrams, tokenize(preprocess(sent)), 2))
  >>> NgramProbs(accum).items()[1:2]
  [('four', {'and': 0.26666666666666666, 'horses': 0.13333333333333333, 'selves': 0.066666666666666666, 'months': 0.066666666666666666, 'o': 0.20000000000000001, 'years': 0.26666666666666666, 'hours': 0.20000000000000001, 'to': 0.066666666666666666, 'miles': 0.13333333333333333, 'servants': 0.066666666666666666, 'weeks': 0.20000000000000001, 'perfectly': 0.066666666666666666, '</s>': 0.066666666666666666, 'children': 0.13333333333333333, 'times': 0.066666666666666666})]
  >>>
  '''
  ngramprobs = {}
  for prefix,freqs in cond_freqs.iteritems():
    ngramprobs[prefix] = {}
    N = float(len(freqs))
    for term, count in freqs.iteritems():
      ngramprobs[prefix][term] = float(count)/N
  return ngramprobs

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  
