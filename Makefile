POSTAGGER=/Users/wdxu/tools/stanford-postagger-2014-10-26

target: data model test

data: data/sentence-id data/pos-tagging data/feature
	mkdir -p data

clean:
	rm -rf log
	rm -rf models
	rm -rf results
	rm -rf data/pos-tagging
	rm -rf data/sentence-id
	rm -rf data/feature

data/sentence-id: data/raw-data/train_data.txt data/raw-data/dev_data.txt data/raw-data/test_data.txt
	mkdir -p data/sentence-id
	python src/gen_sentence_id.py $^ data/sentence-id/id data/sentence-id/sentence

data/pos-tagging: data/pos-tagging/pos
	mkdir -p data/pos-tagging

data/pos-tagging/pos: data/sentence-id/sentence
	mkdir -p data/pos-tagging
	python src/gen_pos.py $^ $@
	#java -mx300m -classpath $(POSTAGGER)/stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model $(POSTAGGER)/models/english-bidirectional-distsim.tagger -textFile $^ > $@

data/feature: data/feature/train_feature.arff data/feature/dev_feature.arff data/feature/test_feature.arff

data/feature/train_feature.arff: data/raw-data/train_data.txt
	mkdir -p data/feature
	python src/Feature_Combiner.py train $^ $@

data/feature/dev_feature.arff: data/raw-data/dev_data.txt data/raw-data/dev_gold.txt
	mkdir -p data/feature
	python src/Feature_Combiner.py dev $^ $@

data/feature/test_feature.arff: data/raw-data/test_data.txt
	mkdir -p data/feature
	python src/Feature_Combiner.py test $^ $@

model: models/RF.15.model
	mkdir -p models

models/RF.15.model: data/feature/train_feature.arff data/feature/dev_feature.arff
	mkdir -p models
	java -cp lib/weka.jar weka.classifiers.trees.RandomForest -t data/feature/train_feature.arff -c first -d $@ -T data/feature/dev_feature.arff -I 15 > log

test: results/RF.15-fea.130.arff results/test_gold.txt
	
results/RF.15-fea.130.arff: models/RF.15.model data/feature/test_feature.arff
	mkdir -p results
	java -cp lib/weka.jar weka.classifiers.trees.RandomForest -t data/feature/train_feature.arff -c first -T data/feature/test_feature.arff -I 15 -classifications weka.classifiers.evaluation.output.prediction.PlainText > $@

results/test_gold.txt: data/raw-data/test_data.txt results/RF.15-fea.130.arff
	mkdir -p results
	python src/gen_answers.py $^ $@
