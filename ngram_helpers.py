#!/usr/bin/env python

import re
from itertools import islice

months = "(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
substitutions = [
  # symbols and emoticons
  (re.compile(r'([\w]+)_[\s]+'), r'\1 '), # remove trailing '_'
  (re.compile(r'_([\w]+)[\s]+'), r'\1 '), # remove leading '_'
  #(re.compile(r'[\"]+([^\"]+)[\"]+'), r'\1 '), # remove embedded double quotes
  (re.compile(r'\s(=\)|\:\)|\: \)|\:\-\)|\:D|<3|\:>|\: >|\:\->)\s'), r' _emoticon_p_ '), # happy emoticon
  (re.compile(r'\s(=\(|\:\(|\: \(|\:\-\(|\:<)\s'), r' _emoticon_n_ '), # sad or neutral emoticons
  # contractions 
  (re.compile(r"(?<=\W)(im|i m|i\'m)(?=\W)",re.I),"i am"), # i'm -> i am
  (re.compile(r"(?<=\W)i\'ll(?=\W)",re.I),"i will"), # i'll -> i will
  (re.compile(r"(?<=\W)i\'ve(?=\W)",re.I),"i have"), # i've -> i have

  (re.compile(r"(?<=\W)you\'*re(?=\W)",re.I),"you are"), # you're -> you are
  (re.compile(r"(?<=\W)you\'*ll(?=\W)",re.I),"you will"), # you'll -> you will
  (re.compile(r"(?<=\W)you\'*ve(?=\W)",re.I),"you have"), # you've -> you have

  (re.compile(r"(?<=\W)she\'ll(?=\W)",re.I),"she will"), # she'll -> she will
  (re.compile(r"(?<=\W)it\'*ll(?=\W)",re.I),"it will"), # it'll -> it will

  (re.compile(r"(?<=\W)we\'re(?=\W)",re.I),"we are"), # we're -> we are
  (re.compile(r"(?<=\W)we\'ll(?=\W)",re.I),"we will"), # we'll -> we will
  (re.compile(r"(?<=\W)we\'*ve(?=\W)",re.I),"we have"), # we've -> we have

  (re.compile(r"(?<=\W)they\'*re(?=\W)",re.I),"they are"), # they're -> they are
  (re.compile(r"(?<=\W)they\'*ll(?=\W)",re.I),"they will"), # they'll -> they will
  (re.compile(r"(?<=\W)they\'*ve(?=\W)",re.I),"they have"), # they've -> they have

  (re.compile(r"(?<=\W)there\'*ll(?=\W)",re.I),"there will"), # there'll -> there will
  (re.compile(r"(?<=\W)that\'*ll(?=\W)",re.I),"that will"), # that'll -> that will

  (re.compile(r"(?<=\W)aren\'*t(?=\W)",re.I),"are not"), # aren't -> are not
  (re.compile(r"(?<=\W)can\'*t(?=\W)",re.I),"can not"), # can't -> can not
  (re.compile(r"(?<=\W)couldn\'*t(?=\W)",re.I),"could not"), # couldn't -> could not
  (re.compile(r"(?<=\W)didn\'*t(?=\W)",re.I),"did not"), # didn't -> did not
  (re.compile(r"(?<=\W)doesn\'*t(?=\W)",re.I),"does not"), # doesn't -> does not
  (re.compile(r"(?<=\W)don\'*t(?=\W)",re.I),"do not"), # don't -> do not
  (re.compile(r"(?<=\W)hadn\'*t(?=\W)",re.I),"had not"), # hadn't -> had not
  (re.compile(r"(?<=\W)hasn\'*t(?=\W)",re.I),"has not"), # hasn't -> has not
  (re.compile(r"(?<=\W)isn\'*t(?=\W)",re.I),"is not"), # isn't -> is not
  (re.compile(r"(?<=\W)mustn\'*t(?=\W)",re.I),"must not"), # mustn't -> must not
  (re.compile(r"(?<=\W)needn\'*t(?=\W)",re.I),"need not"), # needn't -> need not            
  (re.compile(r"(?<=\W)shouldn\'*t(?=\W)",re.I),"should not"), # shouldn't -> should not
  (re.compile(r"(?<=\W)wasn\'*t(?=\W)",re.I),"was not"), # wasn't -> was not
  (re.compile(r"(?<=\W)weren\'*t(?=\W)",re.I),"were not"), # weren't -> were not
  (re.compile(r"(?<=\W)won\'t(?=\W)",re.I),"will not"), # won't -> will not
  (re.compile(r"(?<=\W)wouldn\'*t(?=\W)",re.I),"would not"), # wouldn't -> would not
  
  (re.compile(r"(?<=\W)tryin(?=\W)",re.I),"trying"), # tryin -> trying
  (re.compile(r"(?<=\W)think\'*n(?=\W)",re.I),"thinking"), # think'n -> thinking
  (re.compile(r"(?<=\W)cannot(?=\W)",re.I),"can not"), # cannot -> can not
  (re.compile(r"(?<=\W)what\'*s(?=\W)",re.I),"what is"), # what's -> what is         
  
  (re.compile(r"(?<=\W)n\'t(?=\W)",re.I),"not"), # what's -> what is         
  (re.compile(r"(?<=\W)\'m(?=\W)",re.I),"am"), # what's -> what is         

  (re.compile(r"(?<=\W)\d+/\d+/\d+(?=\W)"),"-date-"), # remove dates
  
  (re.compile(r"(?<=\W)\d+/\d+(?=\W)"),"-date-"), # remove dates
  (re.compile(r"%s\s*\d+\s*,\s*\d+"%months,re.I),"-date-"), # remove dates
  (re.compile(r"(?<=\W)\d*\s*%s\s\d+(?=\W)"%months,re.I),"-date-"), # remove dates

  (re.compile(r"(?<=\W)\d{11,}(?=\W)"),"-digitstring-"), # Order numbers, etc

  (re.compile(r"(?<=\W)\$*\d+\.\d\d(?=\W)"),"-money-"), # remove money ($29.99, 29.99)
  (re.compile(r"(?<=\W)[\+\-]*\$\d+[\.,]*\d+(?=\W)"),"-money-"), # remove money ($100,000 -$5)

  (re.compile(r"(?<=\W)n\'t(?=\W)",re.I),"not"), # what's -> what is         

  (re.compile(r"(?<=\W)hm+(?=\W)",re.I),"hmm"), # normalize hmm, hmmmm, etc
  (re.compile(r"([\s^]+)mm+(?=\W)",re.I),r"\1mmm"), # normalize mm, mmmm, etc
  (re.compile(r"(?<=\W)grr+(?=\W)",re.I),"grr"), # normalize grr, grrrr, etc
  (re.compile(r"(?<=\W)ahh+(?=\W)",re.I),"ahh"), # normalize ahh, ahhhh, etc
  (re.compile(r"(?<=\W)ug+h+(?=\W)",re.I),"ugh"), # normalize ugh
  (re.compile(r":[\-\']*\(+",re.I)," -frown- "), # normalize frown :( and :-(
  (re.compile(r"(\s*):[\-\=]*\)",re.I),r" -smile- "), # normalize smiley :), :-), =), etc

  # Common abbreviations and typos...
  (re.compile(r"http:[\S]+(?=\W)",re.I),"-url-"),
  (re.compile(r"https:[\S]+(?=\W)",re.I),"-url-"),
  (re.compile(r"(?<=\W)zip\s+code(?=\W)",re.I),"zipcode"),
  (re.compile(r"(?<=\W)w/(?=\W)",re.I),"with"),
  (re.compile(r"(?<=\W)b4(?=\W)",re.I),"before"),
  (re.compile(r"(?<=\W)waht(?=\W)",re.I),"what"),
  (re.compile(r'\s(d|da|th|teh)\s'), r' the '),
  (re.compile(r"(?<=\W)lotof(?=\W)",re.I),"lot of"),
  (re.compile(r"(?<=\W)xmas(?=\W)",re.I),"christmas"),
  (re.compile(r"(?<=\W)@(?=\W)",re.I),"at"), # @ -> at
  (re.compile(r"(?<=\W)r(?=\W)",re.I),"are"), # r -> are
  (re.compile(r"^r(?=\W)",re.I),"are"), # r -> are
  (re.compile(r"(?<=\W)u(?=\W)",re.I),"you"), # u -> you
  (re.compile(r"(?<=\W)plz(?=\W)",re.I),"please"), # plz -> please

  (re.compile(r"(?<=\W)#(?=\W)"),"number"), #   # -> number
  (re.compile(r"(?<=[^a-zA-Z0-9])\-(?=[^a-zA-Z0-9])"),""), # - -> Null
  (re.compile(r"(?<=[^a-zA-Z0-9])_(?=[^a-zA-Z0-9])"),""), # _ -> Null
  (re.compile(r"(?<=\W)w\.*t\.*f\.*(?=\W)",re.I),"what the fuck"), #   wtf -> what the fuck
  (re.compile(r"(?<=\W)o\.*m\.*g\.*(?=\W)",re.I),"oh my god"), #   omg -> oh my god
  (re.compile(r"(?<=\W)l\.*m\.*a\.*o\.*(?=\W)",re.I),"laughing my ass off"), #lmao -> laughing my ass off

  # common words with period endings
  (re.compile(r'(mr|mrs|jr|sr|dr)\.\s', re.I), r' \1 '),

  (re.compile(r'\s[-\.,\"]{2,}'), r' '), # remove repeated symbols
  (re.compile(r'([\w]+)[\._<-]{1,}([\w]+)'), r'\1. \2'), # remove symbols separating words
]


def preprocess(input):
  ''' Given an input string run all preprocessing 
  patterns on the string.
  >>> from nltk.data import load
  >>> sent_tok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_tok.tokenize(g.raw('austen-emma.txt'))
  >>> preprocess(sents[4])
  'between them it was more the intimacy\\nof sisters.'
  '''
  input = input.lower()
  for (p,s) in substitutions:
    input = p.sub(s, input)
  #print input
  return input

def is_a_term(term):
  ''' given a candidate term, return True if the candidate meets
  all the criteria of a term and False if not.
  >>> is_a_term(',')
  False
  >>> is_a_term('2345')
  True
  >>> is_a_term('hello world')
  True
  >>>
  '''
  if len(term) > 0 and term[0] is ' ': print term
  if term in ['', ' ']: # spaces
    return False
  if term in [',', ',', '.']: # punctuation
    return False
  for c in term:
    if c in 'abcdefghijklmnopqrstuvwxz0123456789.':
      break
  else: # Note: wierd but cool for...else
    return False
  return True

sentence_splitter = re.compile(r'(\W+)')
def tokenize(input_string):
  ''' given an input sentence, split the sentence 
  into a list of terms, adding begining and end of 
  sentence markers. return a generator to the tokens.
  >>> from nltk.data import load
  >>> sent_tok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_tok.tokenize(g.raw('austen-emma.txt'))
  >>> [w for w in tokenize(preprocess(sents[4]))]
  ['<s>', 'between', 'them', 'it', 'was', 'more', 'the', 'intimacy', 'of', 'sisters', '</s>']
  >>>
  '''
  yield '<s>'
  for word in sentence_splitter.split(input_string):
    word = word.strip()
    if is_a_term(word):
      yield word
  yield '</s>'

def generate_ngrams(sentence, n):
  ''' given a tokenized sentence and an integer,
  generate ngrams of order n from the sentence.
  Return a generator of the ngrams.
  >>> from nltk.data import load
  >>> sent_tok = load('tokenizers/punkt/english.pickle')
  >>> from nltk.corpus import gutenberg as g
  >>> sents = sent_tok.tokenize(g.raw('austen-emma.txt'))
  >>> [ng for ng in generate_ngrams(tokenize(preprocess(sents[4])), 2)]
  [['<s>', 'between'], ['between', 'them'], ['them', 'it'], ['it', 'was'], ['was', 'more'], ['more', 'the'], ['the', 'intimacy'], ['intimacy', 'of'], ['of', 'sisters'], ['sisters', '</s>']]
  >>> 
  '''
  words = [word for word in sentence]
  for i in range(len(words) - n + 1):
    ngram = [n_term for n_term in islice(words, i, i + n)]
    yield ngram

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  
