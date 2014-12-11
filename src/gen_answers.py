#!/usr/bin/python

import codecs
import sys

def gen_answers(ifn, afn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	af = codecs.open(afn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')

	sline = sf.readline()

	# read headlines
	aline = af.readline()
	aline = af.readline()
	aline = af.readline()
	aline = af.readline()
	aline = af.readline()
	aline = af.readline()

	while sline and aline:
		answer = aline.split()[2].split(':')[1]
		id_1 = sline.split()[0]
		id_2 = sline.split()[1]
		of.write(answer + '\t' + id_1 + '\t' + id_2 + '\n')

		sline = sf.readline()
		aline = af.readline()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		gen_answers('../data/raw-data/test_data.txt', '../results/SVM.C10-fea.130.arff', '../results/test_gold.txt')
	else:
		gen_answers(sys.argv[1], sys.argv[2], sys.argv[3])
	
