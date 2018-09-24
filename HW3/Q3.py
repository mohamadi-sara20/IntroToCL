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
def SelectLexicon(Filename, Thr):
    words = HW1.CountWordsFile(Filename)
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
    write_data("Lexicon.txt", s)

    return lexicon

#Part 2
def ReplaceOOV(corpus, lexicon, phrase):

    with open(corpus, encoding="UTF-8") as f:
        text = f.read()

    with open(lexicon, encoding="UTF-8-sig") as f:
        vocab = f.read()
    vocab = vocab.split("\n")

    punc = ["(", "[", "“", "«", "{", ")", "\]", "”", "»","!", ",", ";", "؛", ":", "،", "؟"]

    for i in range(len(punc)):
        pat = re.compile(r"([" + punc[i] + "])")
        text = re.sub(pat, r" \1 ", text)

    pat = re.compile(r"([.:؛])( )+")
    text = re.sub(pat, r" </s>\2" , text)
    text = (text.split(" </s>"))

    with open("ZebraAllNormalizedOOV.txt", "w+", encoding="UTF-8-sig") as f:
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

    with open("ZebraAllNormalizedOOV.txt", encoding="UTF-8-sig") as f:
        text = f.read()

    return text

t = ReplaceOOV("ZebraAllNormalized.txt", "Lexicon.txt", "خاو")

#Part 3
def CalculateMonoGram(ZebraAllNormalizedOOV, Lexicon):
    with open(ZebraAllNormalizedOOV, encoding="UTF-8-sig") as f:
        s = f.readlines()
        n = len(s)

    freq = HW1.CountWordsFile(ZebraAllNormalizedOOV)

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

    with open("LexiconMonoGram.txt", "w+", encoding='UTF-8-sig') as f:
        for p in probs:
            f.write(p[0])
            f.write("\t")
            f.write(str(p[1]))
            f.write("\n")

    return probs


y = CalculateMonoGram("ZebraAllNormalizedOOV.txt", "Lexicon.txt")

#Part4
def CalculateBiGram(ZebraAllNormalizedOOV, Lexicon):

    with open(ZebraAllNormalizedOOV, encoding="UTF-8-sig") as f:
        text = f.read()
        punc = ["(", "[", "“", "«", "{", ")", "\]", "”", "»", "!", ",", ";", "؛", ":", "،", "؟"]
        for i in range(len(punc)):
            pat = re.compile(r"[" + punc[i] + "]")
            text = re.sub(pat, r"", text)
        text = text.split("\n")

    bigrams = {}
    with open(Lexicon, encoding="UTF-8-sig") as f:
        lexicon = f.read()
        lexicon = lexicon.split("\n")


    freq = HW1.CountWordsFile(ZebraAllNormalizedOOV)

    with open(ZebraAllNormalizedOOV, encoding="UTF-8-sig") as f:
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

    with open("BiGrams.txt", "w+", encoding="UTF-8-sig") as f:
        for prob in probs:
            element = str(prob[0][0]) + "\t" + str(prob[0][1])
            f.write(element)
            f.write("\t")
            f.write(str(prob[1]))
            f.write("\n")

    return probs


BiGrams = CalculateBiGram("ZebraAllNormalizedOOV.txt", "Lexicon.txt")


#Part5
def KN(ZebaAllNormalizedOOV, Lexicon):
    text = read_data(ZebaAllNormalizedOOV)
    text_list = text.split()
    lexicon = read_data(Lexicon)
    words = lexicon.split("\n")

    word_counts = {}
    for word in text_list:
        word_counts[word] = word_counts.get(word, 0) + 1
    words_before = {}
    bi_grams1 = {}
    previous_word = text_list[0]
    for i in range(1, len(text_list)):
        word = text_list[i]
        pair = previous_word + " " + word
        if pair not in bi_grams1:
            bi_grams1[pair] = 1
            words_before[word] = 1
        else:
            bi_grams1[pair] += 1
        previous_word = word

    words_after = {}
    bi_grams2 = {}
    next_word = text_list[1]
    for i in range(len(text_list)-1):
        word = text_list[i]
        pair = word + " " + next_word
        if pair not in bi_grams2:
            bi_grams2[pair] = 1
            words_after[word] = 1
        else:
            bi_grams2[pair] += 1

        next_word = text_list[i + 1]
    p_continuation = {}
    for key in words_before:
        p_continuation[key] = round(Decimal(words_before[key]) / Decimal(len(bi_grams1)), 6)

    landa = {}
    for word in words_after:
        landa[word] = round(Decimal(0.75) * Decimal(words_after[word]) / Decimal(word_counts[word]), 6)

    p_kenser_ney = {}
    for i in range(len(text_list) - 1):
        first_word = text_list[i]
        second_word = text_list[i + 1]
        pair = first_word + " " + second_word
        max = 0
        temp = 0
        if first_word + " " + second_word in bi_grams2:
            temp = bi_grams2[first_word + " " + second_word] - 0.75
        if temp > 0:
            max = temp
        if pair not in p_kenser_ney:
            p_kenser_ney[pair] = round(p_continuation[second_word] * landa[first_word] * Decimal(max) / Decimal(
                word_counts[first_word]), 6)

    s = ""
    for key, value in p_kenser_ney.items():
        s += str(key)+"\t"+ str(value) + "\n"
    write_data("BiGramsKN.txt", s)

    return

print(KN("ZebraAllNormalizedOOV.txt", "Lexicon.txt"))


