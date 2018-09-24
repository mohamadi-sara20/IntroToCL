from math import log2
import re

with open("Tags.txt", encoding="UTF8") as f:
    tags = f.read().split("\n")
    tags.pop()


def MyLog(num):
    if num == 0:
        return -1000000
    return log2(num)


def SentenceNormalizer(sentence):

    punc = ["(",".", "[", "“", "«", "{", ")", "\]", "”", "»", "!", ",", ";", "؛", ":", "،", "؟"]
    for p in punc:
        f_pat = re.compile('([' + p + '])')
        sentence = re.sub(f_pat, r" \1 ", sentence)
    return sentence


def MyViterbi(sentence, states, init_prob, trans_probab, emission_prob):

    sentence = sentence.split("~")
    viterbi = [{}]
    path = {}

    for state in states:
        viterbi[0][state] = MyLog(float(init_prob[state])) + MyLog(float(emission_prob[(state, sentence[0])]))
        path[state] = [state]

    for sentence_index in range(1, len(sentence)):
        viterbi.append({})
        new_path = {}
        for state in states:
            probability, possible_state = max(
                [(viterbi[sentence_index-1][y0] + MyLog(float(trans_probab[(y0, state)]))
              + MyLog(float(emission_prob[(state,sentence[sentence_index])])), y0) for y0 in states])
            viterbi[sentence_index][state] = probability
            new_path[state] = path[possible_state] + [state]

        path = new_path
    probability, state = max([(viterbi[len(sentence) - 1][state], state) for state in tags])

    return path[state]


def MyPOSTagger(TestSent, ProbsPi, ProbsA, ProbsB):

    with open(ProbsPi, encoding="UTF8") as f:
        pi = f.read().split("\n")
        pi.pop()
        pi_dic = {}
        for item in pi:
            item = item.split()
            pi_dic[item[0]] = item[1]

    with open(ProbsA, encoding="UTF8") as f:
        transProbs = f.read().split("\n")
        transProbs.pop()
        transProbs_dic = {}
        for item in transProbs:
            item = item.split("\t")
            x, y = item[0].split()
            transProbs_dic[(x, y)] = item[1]

    with open(ProbsB, encoding="UTF8")as f:
        emisProbs = f.read().split("\n")
        emisProbs.pop()
        emisProb_dic = {}
        for item in emisProbs:
            item = item.split("\t")
            emisProb_dic[(item[0], item[1])] = item[2]

    allTags = []
    output = ""
    with open(TestSent, encoding="UTF8") as f:
        test = f.read()
        words = test.split("\n")
        words.pop()

    while "." in words:
        ind = words.index(".")
        s = words[:ind+1]
        sentence = "~".join(s)
        predicted_tags = (MyViterbi(sentence, tags, pi_dic, transProbs_dic, emisProb_dic))
        allTags += predicted_tags
        words = words[ind+1:]

        for i in range(len(s)):
            output += s[i] + "\t" + predicted_tags[i] + "\n"

    with open("POST-Persian-Corpus-Test-MyOut.txt", "w+", encoding="UTF8") as f:
        f.write(output)

    return allTags


def CalculatePOSTAccuracy(TrueTags, EstimatedTags):
    with open(TrueTags, encoding="UTF8") as f:
        text = f.read()
        text = re.sub(r"              *", "~", text)
        text = text.split("\n")
        text.pop()

        test_tags = []
        for item in text:
            item = item.split("~")
            test_tags.append(item[1])

    estimated_tags = []
    with open(EstimatedTags, encoding="UTF8") as f:
        output = f.read().split("\n")
        output.pop()

        for item in output:
            item = item.split("\t")
            estimated_tags.append(item[1])

    c = 0
    for i in range(len(test_tags)):
        if test_tags[i] == estimated_tags[i]:
            c += 1
    accuracy = c / len(test_tags)

    return accuracy

allTags = MyPOSTagger("POST-Persian-Corpus-Test-Sent.txt", "ProbsPi.txt", "ProbsA.txt", "ProbsB.txt")
print(CalculatePOSTAccuracy("POST-Persian-Corpus-Test.txt", "POST-Persian-Corpus-Test-MyOut.txt"))

