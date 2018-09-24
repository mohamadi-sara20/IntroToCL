from math import log2, pow
from operator import itemgetter
import os
import re
import CombineFiles, CorrectVariations, CorrectPuncs, CorrectCodings, Q3
train, test = CombineFiles.CombineFiles("ZebRa", 8)
train_path = "Train/"
test_path = "Test/"
if not os.path.exists(train_path):
    os.makedirs(train_path)

if not os.path.exists(test_path):
    os.makedirs(test_path)

with open("Train/Train.txt", "w+", encoding="UTF-8") as f:
    f.write(train)
with open("Test/Test.txt", "w+", encoding="UTF-8") as f:
    f.write(test)


train1 = CorrectPuncs.CorrectPuncs("Train/","Train.txt")
train2 = CorrectCodings.CorrectCodings("Train/", "ZebraAllPuncs.txt", "TableCodings.txt")
train3 = CorrectVariations.CorrectVariations("Train/", "ZebraAllCoding.txt", "TableVariations.txt")

train_Lexicon = Q3.SelectLexicon("Train/", "ZebraAllNormalized.txt", 3)
train_CorpusOOV = Q3.ReplaceOOV("Train/", "ZebraAllNormalized.txt", "Train/Lexicon.txt", "خاو")
train_monograms = Q3.CalculateMonoGram("Train/", "ZebraAllNormalizedOOV.txt", "Train/Lexicon.txt")

test1 = CorrectPuncs.CorrectPuncs("Test/", "Test.txt")
test2 = CorrectCodings.CorrectCodings("Test/", "ZebraAllPuncs.txt", "TableCodings.txt")
test3 = CorrectVariations.CorrectVariations("Test/", "ZebraAllCoding.txt", "TableVariations.txt")

test_CorpusOOV = Q3.ReplaceOOV("Test/", "ZebraAllNormalized.txt", "Train/Lexicon.txt", "خاو")
test_monograms = Q3.CalculateMonoGram("Test/", "ZebraAllNormalizedOOV.txt", "Train/Lexicon.txt")

def CalculateSentenceProbability(sentence, monograms):
    sentence_log_probability = 0
    for word in sentence:
        if word in monograms:
            if word != "<s>" and word != "</s>":
                word_probability = monograms[word]
                if word_probability != 0:
                    sentence_log_probability += log2(float(word_probability))

    return sentence_log_probability


def CalculateMonoGramPerplexity(TestPerplexity, LexiconMonoGram):
    with open(LexiconMonoGram, encoding="UTF-8") as f:
        train_monograms = f.read()[1:]
        train_monograms = train_monograms.split("\n")
        train_monograms = train_monograms[:len(train_monograms)-2]

    monograms = {}
    for item in train_monograms:
        item = item.split()
        monograms[item[0]] = item[1]

    with open(TestPerplexity, "r", encoding="UTF-8") as f:
        sentences = f.read()[1:]
        sentences = sentences.split("\n")

    monogram_count = 0
    sentence_log_probability = 0
    for sentence in sentences:
        sentence = sentence.split()
        sentence_log_probability += CalculateSentenceProbability(sentence, monograms)
        monogram_count += len(sentence) - 2

    monogram_perplexity = pow(2, -sentence_log_probability / monogram_count)

    return monogram_perplexity

def SentenceNormalizer(sentence):

    punc = ["(", "[", "“", "«", "{", ")", "\]", "”", "»", "!", ",", ";", "؛", ":", "،", "؟"]
    for p in punc:
        f_pat = re.compile(r'[' + p + ']')
        sentence = re.sub(f_pat, " ", sentence)

    return sentence


def calculate_bigram_sentence_probability(sentence, normalizedBigrams, lexicon):
    bigram_sentence_log_probability = 0
    previousIndex = -1
    for word in sentence:
        wordIndex = lexicon.index(word)
        if previousIndex != -1:
            bigram_word_probability = normalizedBigrams[previousIndex][wordIndex]
            bigram_sentence_log_probability += log2(float(bigram_word_probability))
        previousIndex = wordIndex
    return bigram_sentence_log_probability

def CalculateBigramPerplexity(TestFile, TrainNormalizedCorpus, TrainLexiconFile ):
    with open(TestFile, encoding="UTF-8") as f:
        sentences = f.read()[1:]
        sentences = sentences.split("\n")

    normalizedBiGram, lexicon = Q3.CalculateNormalizedBiGram(TrainNormalizedCorpus, TrainLexiconFile)

    bigram_sentence_log_probability = 0
    bigram_count = 0
    for sentence in sentences:
        sentence = SentenceNormalizer(sentence)
        sentence = sentence.split()
        bigram_sentence_log_probability += calculate_bigram_sentence_probability(sentence, normalizedBiGram, lexicon)
        bigram_count += len(sentence) - 1

    return pow(2, -bigram_sentence_log_probability/ bigram_count)

bigram_perplexity = CalculateBigramPerplexity("Test/ZebraAllNormalizedOOV.txt","Train/ZebraAllNormalizedOOV.txt", "Train/Lexicon.txt")
monogram_perplexity = CalculateMonoGramPerplexity("Test/ZebraAllNormalizedOOV.txt", "Train/LexiconMonoGram.txt")
with open("PerplexityOutFile.txt", "w+", encoding="UTF8") as f:
    f.write("MonoGram Perplexity: " + str(monogram_perplexity) + '\n')
    f.write("BiGram Perplexity: " + str(bigram_perplexity))
