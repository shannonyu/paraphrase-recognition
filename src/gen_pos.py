import codecs
import sys
import nltk
import json

def gen_pos(ifn, tfn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	tf = codecs.open(tfn, 'w', 'utf-8')

	line = sf.readline()
	while line:
		line = line.strip()
		tokens = nltk.word_tokenize(line)
		tagged = nltk.pos_tag(tokens)
		tagged_json = json.dumps(tagged)
		tf.write(tagged_json)
		tf.write('\n')
		line = sf.readline()

	return

if __name__ == '__main__':
	if len(sys.argv) == 1:
		gen_pos('../data/sentence-id/sentence', '../data/pos-tagging/pos')
	else:
		gen_pos(sys.argv[1], sys.argv[2])
