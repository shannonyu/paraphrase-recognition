#!/usr/bin/python

import codecs
import sys

def gen_sentence_id(trnfn, devfn, testfn, dfn, sfn):
	df = codecs.open(dfn, 'w', 'utf-8')
	sf = codecs.open(sfn, 'w', 'utf-8')
	sentences = load_data(trnfn, devfn, testfn)

	for key in sentences.keys():
		df.write(key)
		df.write('\n')
		sf.write(sentences[key] )
		sf.write('\n')
	
	return 0

def load_data(trnfn, devfn, testfn):
	sentences = {}
	load_trndata(trnfn, sentences)
	load_devdata(devfn, sentences)
	load_testdata(testfn, sentences)
	return sentences

def load_trndata(ifn, sentences):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()
	if line[0:1].encode('utf-8') == codecs.BOM_UTF8:
		line = line[1:]

	while line:
		number = (line.split('\t')[0])
		sentence1_id = (line.split('\t')[1])
		sentence2_id = (line.split('\t')[2])
		sentence1 = line.split('\t')[3].strip()
		sentence2 = line.split('\t')[4].strip()

		if sentence1_id in sentences and sentences[sentence1_id] != sentence1:
			print 'error'
		if sentence2_id in sentences and sentences[sentence2_id] != sentence2:
			print 'error'
		sentences[sentence1_id] = sentence1
		sentences[sentence2_id] = sentence2

		line = sf.readline()

def load_devdata(ifn, sentences):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()

	if line[0:1].encode('utf-8') == codecs.BOM_UTF8:
		line = line[1:]

	while line:
		sentence1_id = (line.split('\t')[0])
		sentence2_id = (line.split('\t')[1])
		sentence1 = line.split('\t')[2].strip()
		sentence2 = line.split('\t')[3].strip()
		if sentence1_id in sentences and sentences[sentence1_id] != sentence1:
			print 'error'
		if sentence2_id in sentences and sentences[sentence2_id] != sentence2:
			print 'error'

		sentences[sentence1_id] = sentence1
		sentences[sentence2_id] = sentence2

		line = sf.readline()
	

def load_testdata(ifn, sentences):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()

	if line[0:1].encode('utf-8') == codecs.BOM_UTF8:
		line = line[1:]

	while line:
		sentence1_id = (line.split('\t')[0])
		sentence2_id = (line.split('\t')[1])
		sentence1 = line.split('\t')[2].strip()
		sentence2 = line.split('\t')[3].strip()

		if sentence1_id in sentences and sentences[sentence1_id] != sentence1:
			print 'error'
		if sentence2_id in sentences and sentences[sentence2_id] != sentence2:
			print 'error'
		sentences[sentence1_id] = sentence1
		sentences[sentence2_id] = sentence2

		line = sf.readline()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		gen_sentence_id(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
	else:
		gen_sentence_id('../data/raw-data/train_data.txt',\
				'../data/raw-data/dev_data.txt',\
				'../data/raw-data/test_data.txt',\
				'../data/sentence-id/id',\
				'../data/sentence-id/sentence')
