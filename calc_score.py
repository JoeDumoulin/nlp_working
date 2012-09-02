#!/usr/bin/env python

from load_att_file import readchats
from ngram_helpers import preprocess, tokenize
from additive_smoothing import AdditiveSmoothing
from knesser_ney import KnesserNey
from evaluation import cross_entropy
from load_att_file import readchats
from unicodeCSV import UnicodeCSVReader
import codecs

#from nltk.data import load
#from nltk.corpus import gutenberg as g

def get_co_united_chat(row):
  return [w for w in tokenize(preprocess(row[0][129:]))]

def get_chat(line):
  start = line.find(' ') + 1
  return [w for w in tokenize(preprocess(line[start:]))]

def test_pass(model, data, ltrain=10000, ltest=10000):
  train = data[:ltrain]
  #test = data[ltrain:ltrain+ltest]
  test = data[ltest:]
  model.generate_model(train)
  return cross_entropy(model, test)

def check(line):
    if line is not None and line.strip() != '<s> </s>':
      return True
    return False

if __name__ == '__main__':
#  stok = load('tokenizers/punkt/english.pickle')
#  train = [[w for w in tokenize(preprocess(sent))] for sent in stok.tokenize(g.raw('austen-emma.txt'))]
#  test1 = [[w for w in tokenize(preprocess(sent))] for sent in stok.tokenize(g.raw('austen-sense.txt'))]
#  test2 = [[w for w in tokenize(preprocess(sent))] for sent in stok.tokenize(g.raw('austen-persuasion.txt'))]

#  chatlines = [get_chat(line) for line in readchats('out.txt')]
#  print 'total number of chats is %d' %len(chatlines)
#  train = chatlines[:30000]
#  test1 = chatlines[30000:40000]
#  test2 = chatlines[30000:50000]
#
#  a_s = AdditiveSmoothing(n=2)
#
#  with open('filterchats/Res3.csv', 'r') as f:
#    reader = UnicodeCSVReader(f, encoding = 'utf-16')
#    print 'getting chats'
#    chatlines = []
#    with codecs.open('coChats.txt', 'w', encoding='utf-8') as g:
#      for row in reader:
#        chat = get_co_united_chat(row)
#        g.write('%s\n' % u' '.join(chat))
#        chatlines.append(chat)

  with open('coChats.txt', 'r') as f:
    print 'reading chats'
    chatlines = []
    for line in f:
      line = line.strip()
      if check(line):
        chatlines.append([w for w in line.split(' ')])
    #print chatlines
    print '%d chats retrieved' % len(chatlines)
    print 'test Additive Smoothing bigrams using 10,000 training chats and 10,000 test chats'
    print test_pass(AdditiveSmoothing(n=2), chatlines)
    print 'test Additive Smoothing bigrams using 50,000 training chats and 10,000 test chats'
    print test_pass(AdditiveSmoothing(n=2), chatlines, ltrain=50000)
    print 'test Additive Smoothing bigrams using 100,000 training chats and 10,000 test chats'
    print test_pass(AdditiveSmoothing(n=2), chatlines, ltrain=100000)
    print 'test Additive Smoothing bigrams using 500,000 training chats and 10,000 test chats'
    print test_pass(AdditiveSmoothing(n=2), chatlines, ltrain=500000)


    print 'test Knesser-Ney bigrams using 10,000 training chats and 10,000 test chats'
    print test_pass(KnesserNey(n=2), chatlines)
    print 'test Additive Smoothing bigrams using 50,000 training chats and 10,000 test chats'
    print test_pass(KnesserNey(n=2), chatlines, ltrain=50000)
    print 'test Additive Smoothing bigrams using 100,000 training chats and 10,000 test chats'
    print test_pass(KnesserNey(n=2), chatlines, ltrain=100000)
    print 'test Additive Smoothing bigrams using 500,000 training chats and 10,000 test chats'
    print test_pass(KnesserNey(n=2), chatlines, ltrain=500000)
    
#    train = chatlines[:500000]
#    test1 = chatlines[600000:640000]
#    test2 = chatlines[400000:450000]
#
#    a_s = AdditiveSmoothing(n=2)
#    kn = KnesserNey(n=2)
#    #generate and test some models
#    a_s.generate_model(train)
#    kn.generate_model(train)
#    print 'additive smoothing test'
#    print cross_entropy(a_s, test1)
#    #print cross_entropy(a_s, test2)
#
#    print 'knesser-ney test'
#    print cross_entropy(kn, test1)
#    #print cross_entropy(kn, test2)
#
