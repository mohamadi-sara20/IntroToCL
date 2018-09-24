import re
import CorrectCodings
def CalculateEmisProb(TrainCorpus, Tags, Lexicon):
    with open(TrainCorpus, encoding="UTF8") as f:
        train = f.read()
        train = re.sub(r"              *", "\t", train)
        train = train.split("\n")


    with open(Lexicon, encoding="UTF8") as f:
        lexicon = f.read()
        lexicon = lexicon.split("\n")
        lexicon.pop()
    with open(Tags, encoding="UTF8") as f:
        tags = f.read()
        tags = tags.split("\n")
        tags.pop()

    tagged_words = {}
    tag_counts = {}
    for item in train:
        item = item.split("\t")
        tagged_words[(item[0], item[1])] = tagged_words.get((item[0], item[1]), 0) + 1
        tag_counts[item[1]] = tag_counts.get(item[1], 0) + 1

    EmissionProbabilities = []
    for word in lexicon:
        for tag in tags:
            if (word, tag) in tagged_words:
                EmisProb = tagged_words[(word,tag)] / tag_counts[tag]
                EmissionProbabilities.append((tag, word, EmisProb))
            else:
                EmisProb = 0.0
                EmissionProbabilities.append((tag, word, EmisProb))
    return EmissionProbabilities

EmissionProbabilities = CalculateEmisProb("POST-Persian-Corpus-Train.txt", "Tags.txt", "Lexicon.txt")

with open("ProbsB.txt", "w+", encoding="UTF8") as f:
    for item in EmissionProbabilities:
        f.write(item[0] + "\t"  + item[1] + "\t" + str(item[2]) + "\n")
