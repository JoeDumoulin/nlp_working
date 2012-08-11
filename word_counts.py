#!/usr/bin/env python

def Freqs(term_generator, doc, n):
  freqs = {}
  for t in term_generator(doc, n):
    term = (' ').join(t)
    if term not in freqs:
      freqs[term] = 0.0
    freqs[term] += 1.0
  return freqs

def AccumFreqs(acc, freqs):
  for w,c in freqs.iteritems():
    if w not in acc:
      acc[w] = 0.0
    acc[w] += c
  return acc

def TermProb(freqs):
  termprobs = {}
  N = float(len(freqs))
  for term,counts in freqs.iteritems():
    termprobs[term] = float(counts)/N
  return termprobs

def CondFreqs(term_generator, doc, n):
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
  for p,s in cfreqs.iteritems():
    if p not in acc:
      acc[p] = {}
    for w,c in s.iteritems():
      if w not in acc[p]:
        acc[p][w] = 0.0
      acc[p][w] += c
  return acc

def NgramProbs(cond_freqs):
  ngramprobs = {}
  for prefix,freqs in cond_freqs.iteritems():
    ngramprobs[prefix] = {}
    N = float(len(freqs))
    for term, count in freqs.iteritems():
      ngramprobs[prefix][term] = float(count)/N
  return ngramprobs

