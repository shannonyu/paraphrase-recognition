#!/usr/bin/python

import codecs
import sys
from Pair_Generator import *
from Feature_Generator import *

class Feature_Combiner(object):
	def __init__(self, dfn, sfn):
		self.pg = Pair_Generator(dfn, sfn)
		self.fg = Feature_Generator()
		return None

	def combine_trn_features(self, ifn, ofn):
		sf = codecs.open(ifn, 'r', 'utf-8')
		of = codecs.open(ofn, 'w', 'utf-8')

		line = sf.readline()
		if line[0:1].encode('utf-8') == codecs.BOM_UTF8:
			line = line[1:]

		of.write('@relation train\n')
		of.write('@attribute answer {0,1}\n')
		for i in range(self.pg.get_pair_number()):
			for j in range(self.fg.get_feature_number()):
				of.write('@attribute ' + str(i) + '.' + str(j) + ' real\n')
			if i < 4:
				for j in range(self.fg.get_feature_number() + 1):
					of.write('@attribute e' + str(i) + '.' + str(j) + ' real\n')
		of.write('@data\n')

		while line:	
			number = line.split('\t')[0]
			sentence1_id = line.split('\t')[1]
			sentence2_id = line.split('\t')[2]
			sentence1 = line.split('\t')[3]
			sentence2 = line.split('\t')[4]
	
			features = self.gen_pairs_features(sentence1_id, sentence2_id)

			line = sf.readline()
			of.write(number + ',')
			for feature in features:
				of.write(str(feature))
				of.write(',')
			of.write('\n')


	def combine_dev_features(self, ifn, afn, ofn):
		sf = codecs.open(ifn, 'r', 'utf-8')
		af = codecs.open(afn, 'r', 'utf-8')
		of = codecs.open(ofn, 'w', 'utf-8')

		aline = af.readline()

		aline = af.readline()
		line = sf.readline()
		if line[0:1].encode('utf-8') == codecs.BOM_UTF8:
			line = line[1:]

		of.write('@relation dev\n')
		of.write('@attribute answer {0,1}\n')
		for i in range(self.pg.get_pair_number()):
			for j in range(self.fg.get_feature_number()):
				of.write('@attribute ' + str(i) + '.' + str(j) + ' real\n')
			if i < 4:
				for j in range(self.fg.get_feature_number() + 1):
					of.write('@attribute e' + str(i) + '.' + str(j) + ' real\n')
		of.write('@data\n')

		while line:	
			number = aline.split('\t')[0]
			sentence1_id = line.split('\t')[0]
			sentence2_id = line.split('\t')[1]
			sentence1 = line.split('\t')[2]
			sentence2 = line.split('\t')[3]
	
			features = self.gen_pairs_features(sentence1_id, sentence2_id)
			aline = af.readline()
			line = sf.readline()
			of.write(number + ',')
			for feature in features:
				of.write(str(feature))
				of.write(',')
			of.write('\n')


	def combine_test_features(self, ifn, ofn):
		sf = codecs.open(ifn, 'r', 'utf-8')
		of = codecs.open(ofn, 'w', 'utf-8')

		line = sf.readline()
		if line[0:1].encode('utf-8') == codecs.BOM_UTF8:
			line = line[1:]


		of.write('@relation test\n')
		of.write('@attribute answer {0,1}\n')
		for i in range(self.pg.get_pair_number()):
			for j in range(self.fg.get_feature_number()):
				of.write('@attribute ' + str(i) + '.' + str(j) + ' real\n')
			if i < 4:
				for j in range(self.fg.get_feature_number() + 1):
					of.write('@attribute e' + str(i) + '.' + str(j) + ' real\n')
		of.write('@data\n')

		while line:	
			sentence1_id = line.split('\t')[0]
			sentence2_id = line.split('\t')[1]
			sentence1 = line.split('\t')[2]
			sentence2 = line.split('\t')[3]
	
			features = self.gen_pairs_features(sentence1_id, sentence2_id)
			line = sf.readline()
			of.write('1,')
			for feature in features:
				of.write(str(feature))
				of.write(',')
			of.write('\n')


	def gen_pairs_features(self, id_1, id_2):
		features = []
		cnt = 0
		for line1, line2 in self.pg.generate_pairs(id_1, id_2):
			#print line1
			#print line2
			features.extend(self.fg.generate_features(line1, line2))
			if cnt < 4: 
				features.extend(self.gen_substr_features(line1, line2))
			cnt += 1
		return features


	def gen_substr_features(self, line1, line2):
		if len(line1) > len(line2):
			temp = line1
			line1 = line2
			line2 = temp
		#print line1
		#print line2
		sub_cnt = 0
		sum_score = 0
		max_score = 0
		max_substring = ''
		max_features = []
		for i in xrange(0, len(line2) - len(line1) + 1):
			substr_line2 = line2[i: i+len(line1)]
			feature_temp = self.fg.generate_features(line1, substr_line2)
			temp_score = 0
			for feature in feature_temp:
				temp_score += feature
			sum_score += temp_score
			if temp_score >= max_score:
				max_score = temp_score
				max_features = feature_temp
				max_substring = substr_line2
			sub_cnt += 1
		max_features.append(max_score/max(sub_cnt, 1))
		if len(max_features) != 10:
			exit()
		return max_features



if __name__ == '__main__':
	if len(sys.argv) == 1:
		cb = Feature_Combiner('../data/sentence-id/id', '../data/pos-tagging/pos')
		cb.combine_trn_features('../data/raw-data/train_data.txt', '../data/feature/train_feature.arff')
		cb.combine_dev_features('../data/raw-data/dev_data.txt', '../data/raw-data/dev_gold.txt', '../data/feature/dev_feature.arff')
		cb.combine_test_features('../data/raw-data/test_data.txt', '../data/feature/test_feature.arff')
	else:
		cb = Feature_Combiner('data/sentence-id/id', 'data/pos-tagging/pos')
		if sys.argv[1] == 'train':
			cb.combine_trn_features(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == 'dev':
			cb.combine_dev_features(sys.argv[2], sys.argv[3], sys.argv[4])
		elif sys.argv[1] == 'test':
			cb.combine_test_features(sys.argv[2], sys.argv[3])
