import re
import CorrectCodings

def CalculateInitProb(TrainCorpus):
    with open(TrainCorpus, encoding="UTF-8") as f:
        corpus = f.read()
        corpus = re.sub(r"              *", "\t", corpus)
        corpus = corpus.split("\n")
        corpus.pop()

    tags = []
    words = []
    for item in corpus:
        item = item.split("\t")
        tags.append(item[1])
        words.append(item[0])

    allTags = {}
    for tag in tags:
        allTags[tag] = 0


    tag_list = [tags[0]]
    while "." in words:
        ind = words.index(".")
        tag_list.append(tags[ind+1])
        words = words[ind+1:]
        tags = tags[ind+1:]

    for tag in tag_list:
        for t in allTags:
            if t not in tag_list:
                tag_list.append(t)

    numerators = {}
    for item in tag_list:
        numerators[item] = numerators.get(item, 0) + 1
    ProbsPi = []
    for key in numerators:
        if numerators[key] != 1:
            ProbsPi.append((key, numerators[key]/len(tag_list)))
        else:
            ProbsPi.append((key, 0/len(tag_list)))
    print(ProbsPi)
    return ProbsPi

ProbsPi = CalculateInitProb("POST-Persian-Corpus-Train.txt")

with open("ProbsPi.txt", "w+", encoding="UTF8") as f:
    for tag, prob in ProbsPi:
        f.write(tag + "\t" + str(prob) + "\n")
