#!/usr/bin/python

import codecs
import sys
import numpy as np

class Feature_Generator(object):
	def __init__(self):
		return

	def get_edit_distance(self, sentence_1, sentence_2):
		len_1 = len(sentence_1)
		len_2 = len(sentence_2)

		if not len_1 or not len_2:
			return max(len_1, len_2)

		dp = np.zeros([len_1, len_2])
		for i in range(len_1):
			for j in range(len_2):
				dp[i][j] = 1000
		dp[0][0] = 0
		for i in range(len_1):
			for j in range(len_2):
				if i > 0:
					dp[i][j] = min(dp[i][j], dp[i-1][j] + 1)
				if j > 0:
					dp[i][j] = min(dp[i][j], dp[i][j-1] + 1)
				if sentence_1[i] == sentence_2[j]:
					dp[i][j] = min(dp[i][j], dp[i-1][j-1])
				else:
					dp[i][j] = min(dp[i][j], dp[i-1][j-1] + 1)

		return dp[len_1-1][len_2-1]

	def get_jw_distance(self, sentence_1, sentence_2):
		sentence_1 = ''.join(sentence_1)
		sentence_2 = ''.join(sentence_2)
		len_1 = len(sentence_1)
		len_2 = len(sentence_2)

		m = 0
		len_max = max(len_1, len_2)
		match_scope = len_max/2 - 1
		
		match_line_1 = [0] * len_1
		match_line_2 = [0] * len_2

		for i in range(len_1):
			for j in range(max(0, i-match_scope), min(len_2, i+match_scope)):
				if match_line_2[j] == 0 and sentence_1[i] == sentence_2[j]:
					match_line_1[i] = 1
					match_line_2[j] = 1
					m += 1
					break
		
		if m == 0:
			return 0

		result_line_1 = []
		result_line_2 = []

		for i in range(len_1):
			if match_line_1[i]:
				result_line_1.append(sentence_1[i])

		for i in range(len_2):
			if match_line_2[i]:
				result_line_2.append(sentence_2[i])

		
		t = 0
		result_len = len(result_line_1)
		for i in range(result_len):
			if result_line_1[i] != result_line_2[i]:
				t += 1

		l = 0
		while l < len(sentence_1) and l < len(sentence_2) and sentence_1[l] == sentence_2[l]:
			l += 1
		
		dj = m/3.0/len_1 + m/3.0/len_2 + (m-t)/3.0/m
		dw = dj + l*0.1*(1-dj)

		return dw


	def get_onehot_vector(self, sentence_1, sentence_2):
		words = set()
		
		for w in sentence_1:
			words.add(w)
		for w in sentence_2:
			words.add(w)

		x = {}
		y = {}
		for w in words:
			x[w] = 0
			y[w] = 0

		for w in sentence_1:
			x[w] += 1
		for w in sentence_2:
			y[w] += 1

		return x, y


	def get_manhattan_distance(self, sentence_1, sentence_2):
		x, y = self.get_onehot_vector(sentence_1, sentence_2)

		dis = 0
		for w in x.keys():
			dis += max(x[w] - y[w], y[w] - x[w])

		return dis
	

	def get_euclidean_distance(self, sentence_1, sentence_2):
		x, y = self.get_onehot_vector(sentence_1, sentence_2)

		dis = 0
		for w in x.keys():
			dis += (x[w] - y[w]) * (x[w] - y[w])

		return np.sqrt(dis)


	def get_cosine_distance(self, sentence_1, sentence_2):
		x, y = self.get_onehot_vector(sentence_1, sentence_2)

		len_x = 0
		len_y = 0
		
		xy = 0

		keys = x.keys()
		for w in keys:
			len_x += x[w] * x[w]
			len_y += y[w] * y[w]
			xy += x[w] * y[w]
		
		if len_x == 0 or len_y == 0:
			return 0
		return xy/np.sqrt(len_x)/np.sqrt(len_y)
	
	
	def get_ngram_distance(self, sentence_1, sentence_2):
		mod_sentence_1 = []
		mod_sentence_2 = []

		for i in range(len(sentence_1)-2):
			mod_sentence_1.append(' '.join(sentence_1[i:i+3]))

		for i in range(len(sentence_2)-2):
			mod_sentence_2.append(' '.join(sentence_2[i:i+3]))

		return self.get_manhattan_distance(mod_sentence_1, mod_sentence_2)


	def get_matching_coefficient(self, sentence_1, sentence_2):
		x, y = self.get_onehot_vector(sentence_1, sentence_2)

		cnt_xy = 0
		for w in x.keys():
			if x[w] and y[w]:
				cnt_xy += 1

		return cnt_xy


	def get_dice_coefficient(self, sentence_1, sentence_2):
		x, y = self.get_onehot_vector(sentence_1, sentence_2)

		cnt_xy = 0
		cnt_x = 0
		cnt_y = 0
		for w in x.keys():
			if x[w]:
				cnt_x += 1
			if y[w]:
				cnt_y += 1
			if x[w] and y[w]:
				cnt_xy += 1

		if cnt_x + cnt_y == 0:
			return 0

		return 2.0*cnt_xy/(cnt_x + cnt_y)


	def get_jaccard_coefficient(self, sentence_1, sentence_2):
		x, y = self.get_onehot_vector(sentence_1, sentence_2)

		cnt_xy = 0
		for w in x.keys():
			if x[w] and y[w]:
				cnt_xy += 1
		
		if not x.keys():
			return 0

		return 1.0*cnt_xy/len(x.keys())

	def get_feature_number(self):
		return 9

	def generate_features(self, sentence_1, sentence_2):
		features = []
		features.append(self.get_edit_distance(sentence_1, sentence_2))
		features.append(self.get_jw_distance(sentence_1, sentence_2))
		features.append(self.get_manhattan_distance(sentence_1, sentence_2))
		features.append(self.get_euclidean_distance(sentence_1, sentence_2))
		features.append(self.get_cosine_distance(sentence_1, sentence_2))
		features.append(self.get_ngram_distance(sentence_1, sentence_2))
		features.append(self.get_matching_coefficient(sentence_1, sentence_2))
		features.append(self.get_dice_coefficient(sentence_1, sentence_2))
		features.append(self.get_jaccard_coefficient(sentence_1, sentence_2))

		return features

#a = ['who', 'is', 'this']
#b = ['who', 'is', 'that']

#fg = Feature_Generator()
#print fg.get_edit_distance(a,b)
