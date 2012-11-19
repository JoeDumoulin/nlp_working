#!/usr/bin/env python

from load_att_file import readchats
from ngram_helpers import preprocess, tokenize
from additive_smoothing import AdditiveSmoothing
from knesser_ney import KnesserNey
from katz_smoothing import KatzSmoothing
from gt_smoothing import SimpleGoodTuring
from evaluation import cross_entropy
from load_att_file import readchats
from unicodeCSV import UnicodeCSVReader
import codecs


def get_co_united_chat(row):
  return [w for w in tokenize(preprocess(row[0][129:]))]

def get_chat(line):
  start = line.find(' ') + 1
  return [w for w in tokenize(preprocess(line[start:]))]

def test_pass(model, data, ltrain=10000, ltest=10000):
  train = data[:ltrain]
  test = data[ltest:]
  model.generate_model(train)
  return cross_entropy(model, test)

def check(line):
    if line is not None and line.strip() != '<s> </s>':
      return True
    return False

def generate_chatlines(data_path):
  with open(data_path, 'r') as f:
    print 'reading chats'
    for line in f:
      line = line.strip()
      if check(line):
        yield [w for w in line.split(' ')]

def test_austen():
  from nltk.data import load
  from nltk.corpus import gutenberg as g
  stok = load('tokenizers/punkt/english.pickle')
  train = [[w for w in tokenize(preprocess(sent))] for sent in stok.tokenize(g.raw('austen-emma.txt'))]
  test1 = [[w for w in tokenize(preprocess(sent))] for sent in stok.tokenize(g.raw('austen-sense.txt'))]
  test2 = [[w for w in tokenize(preprocess(sent))] for sent in stok.tokenize(g.raw('austen-persuasion.txt'))]

  model1 = AdditiveSmoothing(n=2)
  model1.generate_model(train)
  print 'cross entropy additive smoothing:'
  print 'emma to sense&sensibility: %f0.8' %cross_entropy(model1, test1)
  print 'emma to persuasion: %f0.8' %cross_entropy(model1, test2)
  model2 = KnesserNey(n=2)
  model2.generate_model(train)
  print 'cross entropy knesser-ney smoothing:'
  print 'emma to sense&sensibility: %f0.8' %cross_entropy(model2, test1)
  print 'emma to persuasion: %f0.8' %cross_entropy(model2, test2)
  model3 = SimpleGoodTuring(n=2)
  model3.generate_model(train)
  print 'cross entropy simple good-turing smoothing:'
  print 'emma to sense&sensibility: %f0.8' %cross_entropy(model3, test1)
  print 'emma to persuasion: %f0.8' %cross_entropy(model3, test2)

  model4 = KatzSmoothing(n=2)
  model4.generate_model(train)
  print 'cross entropy katz smoothing:'
  print 'emma to sense&sensibility: %f0.8' %cross_entropy(model4, test1)
  print 'emma to persuasion: %f0.8' %cross_entropy(model4, test2)

def test_model(model, data):
  print '%d chats retrieved' % len(chatlines)
  print 'test bigrams using 10,000 training chats and 10,000 test chats'
  print test_pass(model, data)
  #print 'test bigrams using 50,000 training chats and 10,000 test chats'
#print test_pass(model, data, ltrain=50000)
  #  print 'test Additive Smoothing bigrams using 100,000 training chats and 10,000 test chats'
  #print test_pass(model, data, ltrain=100000)
  #print 'test Additive Smoothing bigrams using 500,000 training chats and 10,000 test chats'
#print test_pass(model, data, ltrain=500000)

def generate_coChats():
  with open('filterchats/Res3.csv', 'r') as f:
    reader = UnicodeCSVReader(f, encoding = 'utf-16')
    print 'getting chats'
    chatlines = []
    with codecs.open('coChats.txt', 'w', encoding='utf-8') as g:
      for row in reader:
        chat = get_co_united_chat(row)
        g.write('%s\n' % u' '.join(chat))

if __name__ == '__main__':
  chatlines = [line for line in  generate_chatlines('coChats.txt')]

  #  test_model(AdditiveSmoothing(n=2), chatlines)
  #test_model(KnesserNey(n=2), chatlines)
#  test_model(SimpleGoodTuring(n=2), chatlines)
  #test_model(KatzSmoothing(n=2), chatlines)

  test_austen()
 
