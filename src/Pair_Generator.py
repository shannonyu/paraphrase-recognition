#!/usr/bin/python

import codecs
import sys
import json
from nltk.stem import SnowballStemmer
from nltk import pos_tag
from util import *

class Pair_Generator:
	def __init__(self, dfn, sfn):
		self.stemmer = SnowballStemmer('english')
		self.sentences = {}
		self.pos_taggings = {}

		self.load_data(dfn, sfn)


	def get_origin_pair(self, id_1, id_2):
		return self.sentences[id_1], self.sentences[id_2]


	def get_stem_pair(self, id_1, id_2):
		words_1 = self.sentences[id_1]
		words_2 = self.sentences[id_2]

		for i in range(len(words_1)):
			words_1[i] = self.stemmer.stem(words_1[i])

		for i in range(len(words_2)):
			words_2[i] = self.stemmer.stem(words_2[i])

		return words_1, words_2


	def get_pos_pair(self, id_1, id_2):
		words_1 = self.pos_taggings[id_1]
		words_2 = self.pos_taggings[id_2]

		return words_1, words_2


	def get_noun_pair(self, id_1, id_2):
		words_1 = self.sentences[id_1]
		words_2 = self.sentences[id_2]
		
		pos_1 = self.pos_taggings[id_1]
		pos_2 = self.pos_taggings[id_2]

		nouns_1 = []
		nouns_2 = []
		for i in range(len(words_1)):
			if pos_1[i][0] == 'N':
				nouns_1.append(words_1[i])

		for i in range(len(words_2)):
			if pos_2[i][0] == 'N':
				nouns_2.append(words_2[i])

		return nouns_1, nouns_2


	def get_verb_pair(self, id_1, id_2):
		words_1 = self.sentences[id_1]
		words_2 = self.sentences[id_2]
		
		pos_1 = self.pos_taggings[id_1]
		pos_2 = self.pos_taggings[id_2]

		verbs_1 = []
		verbs_2 = []
		for i in range(len(words_1)):
			if pos_1[i][0] == 'N':
				verbs_1.append(words_1[i])

		for i in range(len(words_2)):
			if pos_2[i][0] == 'N':
				verbs_2.append(words_2[i])

		return verbs_1, verbs_2


	def get_noun_stem_pair(self, id_1, id_2):
		words_1 = self.sentences[id_1]
		words_2 = self.sentences[id_2]
		
		pos_1 = self.pos_taggings[id_1]
		pos_2 = self.pos_taggings[id_2]

		verbs_1 = []
		verbs_2 = []
		for i in range(len(words_1)):
			if pos_1[i][0] == 'N':
				verbs_1.append(self.stemmer.stem(words_1[i]))

		for i in range(len(words_2)):
			if pos_2[i][0] == 'N':
				verbs_2.append(self.stemmer.stem(words_2[i]))

		return verbs_1, verbs_2
	

	def get_verb_stem_pair(self, id_1, id_2):
		words_1 = self.sentences[id_1]
		words_2 = self.sentences[id_2]
		
		pos_1 = self.pos_taggings[id_1]
		pos_2 = self.pos_taggings[id_2]

		nouns_1 = []
		nouns_2 = []
		for i in range(len(words_1)):
			if pos_1[i][0] == 'V':
				nouns_1.append(self.stemmer.stem(words_1[i]))

		for i in range(len(words_2)):
			if pos_2[i][0] == 'V':
				nouns_2.append(self.stemmer.stem(words_2[i]))

		return nouns_1, nouns_2


	'''
	Retain the first letter of the name and drop all other occurrences of a, e, i, o, u, y, h, w.
	Replace consonants with digits as follows (after the first letter):
		b, f, p, v = 1
		c, g, j, k, q, s, x, z = 2
		d, t = 3
		l = 4
		m, n = 5
		r = 6
	If two or more letters with the same number are adjacent in the original name (before step 1), only retain the first letter; also two letters with the same number separated by 'h' or 'w' are coded as a single number, whereas such letters separated by a vowel are coded twice. This rule also applies to the first letter.
	Iterate the previous step until you have one letter and three numbers. If you have too few letters in your word that you can't assign three numbers, append with zeros until there are three numbers. If you have more than 3 letters, just retain the first 3 numbers.
	'''

	def soundex(self, word):
		if not word:
			return None
		word = word.lower()	
		nocode = 'aeiouyhw'
		one = 'bfpv'
		two = 'cgjkqsxz'
		three = 'dt'
		four = 'l'
		five = 'mn'
		six = 'r'

		sound_map = {}
		for w in nocode:
			sound_map[w] = ''
		for w in one:
			sound_map[w] = '1'
		for w in two:
			sound_map[w] = '2'
		for w in three:
			sound_map[w] = '3'
		for w in four:
			sound_map[w] = '4'
		for w in five:
			sound_map[w] = '5'
		for w in six:
			sound_map[w] = '6'

		temp = ''
		for w in word:
			if is_alphabet(w):
				temp = temp + w
		word = temp
		if not word:
			return '0000'

		while True:
			hasAdj = False
			word_tmp = ''
			idx = 0
			while idx < len(word):
				word_tmp += word[idx]
				while True:
					if sound_map[word[idx]] == '':
						break
					
					#print idx, word[idx], word[idx+1], word[idx+2]
					if idx + 1 < len(word) and sound_map[word[idx]] == sound_map[word[idx + 1]]:
						idx += 1
						hasAdj = True
					elif idx + 2 < len(word) and (word[idx + 1] == 'h' or word[idx + 1] == 'w') and sound_map[word[idx]] == sound_map[word[idx + 2]]:
						idx += 2
						hasAdj = True
					else:
						break
				
				idx += 1


			word = word_tmp
			if not hasAdj:
				break

		soundex = word[0].upper()
		for w in word[1:]:
			soundex = soundex + sound_map[w]
		
		if len(soundex) > 4:
			return soundex[:4]
		else:
			return soundex + '0'*(4-len(soundex))


	def get_soundex_pair(self, id_1, id_2):
		sentence_1 = self.sentences[id_1]
		sentence_2 = self.sentences[id_2]

		soundex_1 = []
		soundex_2 = []

		for word in sentence_1:
			soundex_1.append(self.soundex(word))
		for word in sentence_2:
			soundex_2.append(self.soundex(word))

		return soundex_1, soundex_2


	def get_noun_soundex_pair(self, id_1, id_2):
		nouns_1, nouns_2 = self.get_noun_pair(id_1, id_2)

		soundex_1 = []
		soundex_2 = []
		
		for word in nouns_1:
			soundex_1.append(self.soundex(word))

		for word in nouns_2:
			soundex_2.append(self.soundex(word))

		return soundex_1, soundex_2


	def get_verb_soundex_pair(self, id_1, id_2):
		verbs_1, verbs_2 = self.get_verb_pair(id_1, id_2)

		soundex_1 = []
		soundex_2 = []
		
		for word in verbs_1:
			soundex_1.append(self.soundex(word))

		for word in verbs_2:
			soundex_2.append(self.soundex(word))

		return soundex_1, soundex_2


	def load_data(self, dfn, sfn):
		df = codecs.open(dfn, 'r', 'utf-8')
		sf = codecs.open(sfn, 'r', 'utf-8')

		id_line = df.readline()
		st_line = sf.readline()

		while id_line and st_line:
			if not id_line or not st_line:
				print 'Pair_Generator: load_pos_taggings'
				return

			id_line = id_line.strip()
			st_line = st_line.strip()
			tagged = json.loads(st_line)	
			words = []
			poss = []
			for word in tagged:
				words.append(word[0])
				poss.append(word[1][0])

			self.sentences[id_line] = words
			self.pos_taggings[id_line] = poss

			id_line = df.readline()
			st_line = sf.readline()
		
		return

	def get_pair_number(self):
		return 10

	def generate_pairs(self, id_1, id_2):
		yield self.get_origin_pair(id_1, id_2)
		yield self.get_stem_pair(id_1, id_2)
		yield self.get_pos_pair(id_1, id_2)
		yield self.get_soundex_pair(id_1, id_2)
		yield self.get_noun_pair(id_1, id_2)
		yield self.get_noun_stem_pair(id_1, id_2)
		yield self.get_noun_soundex_pair(id_1, id_2)
		yield self.get_verb_pair(id_1, id_2)
		yield self.get_verb_stem_pair(id_1, id_2)
		yield self.get_verb_soundex_pair(id_1, id_2)

#pg = Pair_Generator('../data/sentence-id/id','../data/pos-tagging/pos')
#print pg.soundex('Pfister')
