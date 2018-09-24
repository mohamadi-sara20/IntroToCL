import re
def CalculateTransProb(TrainCorpus, Tags):
    with open(Tags, encoding="UTF8") as f:
        tags = f.read()
        tags = tags.split("\n")
        tags.pop()

    with open(TrainCorpus, encoding="UTF8") as f:
        train = f.read()
        train = re.sub(r"              *", "\t", train)
        train = train.split("\n")

    tag_sequence = []
    tag_frequency = {}
    for item in train:
        item = item.split("\t")
        tag_sequence.append(item[1])
    for tag in tag_sequence:
        tag_frequency[tag] = tag_frequency.get(tag, 0) + 1

    tag_sequence_dict = {}
    for i in range(len(tag_sequence)-1):
        tag_sequence_dict[(tag_sequence[i], tag_sequence[i+1])]  = tag_sequence_dict.get((tag_sequence[i], tag_sequence[i+1]), 0) + 1

    allTags = {}
    for ftag in tags:
        for stag in tags:
            if (ftag , stag) in tag_sequence_dict:
                allTags[(ftag , stag)] = tag_sequence_dict[(ftag, stag)]
            else:
                allTags[(ftag, stag)] = 0

    AllTagsProbs = {}
    for ftag, stag in allTags:
        AllTagsProbs[(ftag, stag)] = allTags[(ftag, stag)] / tag_frequency[stag]

    return AllTagsProbs

ProbsA = CalculateTransProb("POST-Persian-Corpus-Train.txt", "Tags.txt")
with open("ProbsA.txt", "w+", encoding="UTF8") as f:
    for item in ProbsA:
        f.write(item[0] + " " + item[1] + "\t" + str(ProbsA[item]) + "\n")


