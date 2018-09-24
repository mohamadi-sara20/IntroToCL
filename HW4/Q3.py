from decimal import Decimal
import numpy as np
import operator
import re
import importlib.util
spec = importlib.util.spec_from_file_location("CombineFiles", "CombineFiles.py")
HW1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(HW1)

def read_data(path):
    with open(path, encoding="UTF8") as f:
        text = f.read()
    return text

def write_data(path, text):
    with open(path,"w+", encoding="UTF-8") as f:
        f.write(text)
    return

#Part1
def SelectLexicon(path, Filename, Thr):
    words = HW1.CountWordsFile(path + Filename)
    lexicon = []
    for i in range(len(words[2])):
        if words[2][i][1] >= 3:
            lexicon.append(words[2][i][0])

    to_add = ["<s>", "</s>", "خاو"]
    for i in to_add:
        lexicon.append(i)

    s = ""
    for word in lexicon:
        s += word + "\n"
    write_data(path + "Lexicon.txt", s)

    return lexicon

#Part 2
def ReplaceOOV(path, corpus, lexicon, phrase):

    with open(path + corpus, encoding="UTF-8") as f:
        text = f.read()

    with open(lexicon, encoding="UTF-8-sig") as f:
        vocab = f.read()
    vocab = vocab.split("\n")

    punc = ["(", "[", "“", "«", "{", ")", "\]", "”", "»","!", ",", ";", "؛", ":", "،", "؟"]

    for i in range(len(punc)):
        pat = re.compile(r"([" + punc[i] + "])")
        text = re.sub(pat, r" \1 ", text)

    pat = re.compile(r"([.:؟!?؛])( )+")
    text = re.sub(pat, r" </s>\2" , text)
    #text = (text.split(" </s>"))

    for i in range(len(punc)):
        pat = re.compile(r"([" + punc[i] + "])")
        text = re.sub(pat, r"", text)

    text = (text.split(" </s>"))

    with open(path + "ZebraAllNormalizedOOV.txt", "w+", encoding="UTF-8-sig") as f:
        isFirst = True
        for line in text:
            res = ""
            if isFirst:
                words = line.split()[1:]
                isFirst = False
            else:
                words = line.split()
            import string
            punc = "\)\]”»}\(\[“«{؟،:؛;!,."

            for word in words:
                if word in vocab or word in punc:
                    res += word + " "
                else:
                    res += phrase + " "
            f.write("<s> ")
            f.write(res)
            f.write(" </s>")
            f.write("\n")

    with open(path + "ZebraAllNormalizedOOV.txt", encoding="UTF-8-sig") as f:
        text = f.read()

    return text

#t = ReplaceOOV("ZebraAllNormalized.txt", "Lexicon.txt", "خاو")

#Part 3
def CalculateMonoGram(path, ZebraAllNormalizedOOV, Lexicon):
    with open(path + ZebraAllNormalizedOOV, encoding="UTF-8-sig") as f:
        s = f.readlines()
        n = len(s)

    freq = HW1.CountWordsFile(path + ZebraAllNormalizedOOV)

    with open(Lexicon, encoding="UTF-8-sig") as f:
        lexicon = f.read()
        lexicon = lexicon.split("\n")


    dict = {"<s>":n, "</s>":n}

    for item in freq[2]:
        dict[item[0]] = item[1]

    probs = []
    for word in lexicon:
        if word not in dict.keys():
            p = 0
            probs.append((word, "{0:.10f}".format(p)))
        else:
            p = dict[word] / (freq[0] + 2 * n)
            probs.append((word, "{0:.10f}".format(p)))

    with open(path + "LexiconMonoGram.txt", "w+", encoding='UTF-8-sig') as f:
        for p in probs:
            f.write(p[0])
            f.write("\t")
            f.write(str(p[1]))
            f.write("\n")

    return probs


#y = CalculateMonoGram("ZebraAllNormalizedOOV.txt", "Lexicon.txt")

#Part4
def CalculateBiGram(path, ZebraAllNormalizedOOV, Lexicon):

    with open(path + ZebraAllNormalizedOOV, encoding="UTF-8-sig") as f:
        text = f.read()
        punc = ["(", "[", "“", "«", "{", ")", "\]", "”", "»", "!", ",", ";", "؛", ":", "،", "؟"]
        for i in range(len(punc)):
            pat = re.compile(r"[" + punc[i] + "]")
            text = re.sub(pat, r"", text)
        text = text.split("\n")

    bigrams = {}
    with open(path + Lexicon, encoding="UTF-8-sig") as f:
        lexicon = f.read()
        lexicon = lexicon.split("\n")


    freq = HW1.CountWordsFile(path + ZebraAllNormalizedOOV)

    with open(path + ZebraAllNormalizedOOV, encoding="UTF-8-sig") as f:
        s = f.readlines()
        n = len(s)

    dict = {"<s>":n, "</s>":n}

    for item in freq[2]:
        dict[item[0]] = item[1]

    for line in text:
        line = "<s> " + line + " </s>"
        line = line.split()
        for i in range(len(line)-1):
            bigrams[(line[i], line[i+1])] = bigrams.get((line[i], line[i+1]), 0) + 1


    probs = []
    for bigram in bigrams:
        p = bigrams[bigram] / dict[bigram[0]]
        probs.append((bigram, "{0:.10f}".format(p)))

    '''
    with open("LexiconBigrams.txt", "w+", encoding="UTF-8-sig") as f:
        for i in lexicon:
            for j in lexicon:
                if (i, j) in bigrams.keys():
                    p = bigrams[(i, j)] / dict[i]
                    probability = "{0:.10f}".format(p)
                    element = str(i) + "\t" + str(j)
                    f.write(element)
                    f.write("\t")
                    f.write(str(probability))
                    f.write("\n")
                else:
                    element = str(i) + "\t" + str(j)
                    f.write(element)
                    f.write("\t")
                    f.write("0.0000000000")
                    f.write("\n")
                f.flush()
    '''
    with open(path + "BiGrams.txt", "w+", encoding="UTF-8-sig") as f:
        for prob in probs:
            element = str(prob[0][0]) + "\t" + str(prob[0][1])
            f.write(element)
            f.write("\t")
            f.write(str(prob[1]))
            f.write("\n")

    return probs


#BiGrams = CalculateBiGram("ZebraAllNormalizedOOV.txt", "Lexicon.txt")


def CalculateNormalizedBiGram(InTextFileName, LexiconFile):
    with open(InTextFileName, encoding="utf8") as content:
        text = content.read()[1:]


    with open(LexiconFile, encoding="utf8") as content:
        lexicon = content.read()
    lexicon = lexicon.split("\n")
    lexicon.pop(-1)

    mono_count = np.zeros((len(lexicon)))
    bi_count = np.zeros((len(lexicon), len(lexicon)))

    words = text.split()

    for i in range(len(words) - 1):
        mono_count[lexicon.index(words[i])] += 1
        bi_count[lexicon.index(words[i])][lexicon.index(words[i + 1])] += 1
    mono_count[lexicon.index(words[-1])] += 1

    count_bigram = 0
    for i in range(len(bi_count)):
        for j in range(len(bi_count[i])):
            if bi_count[i][j] > 0:
                count_bigram += 1

    p_continuation = np.zeros((len(lexicon)))
    for i in range(len(p_continuation)):
        for j in range(len(lexicon)):
            if bi_count[j][i] > 0:
                p_continuation[i] += 1
    p_continuation = np.divide(p_continuation, count_bigram)

    d = 0.75

    landa = np.zeros((len(lexicon)))
    for i in range(len(landa)):
        for j in range(len(lexicon)):
            if bi_count[i][j] > 0:
                landa[i] += 1
        if mono_count[i] != 0:
            landa[i] = (d / mono_count[i]) * landa[i]

    bigram = np.zeros((len(lexicon), len(lexicon)))
    for i in range(len(lexicon)):
        for j in range(len(lexicon)):
            if mono_count[i] != 0:
                bigram[i][j] = max([bi_count[i][j] - d, 0]) / mono_count[i] + landa[i] * p_continuation[j]

    return bigram, lexicon


