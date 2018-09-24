import operator

def Mylevenshtein(string1, string2):
    len_s1 = len(string1)
    len_s2 = len(string2)
    if len_s1 == 0 and len_s2 == 0:
        return 0

    else:
        len_sum = float(len_s1 + len_s2)
        chars = []
        for i in range(len_s1 + 1):
            chars.append([i])
        del chars[0][0]

        for j in range(len_s2+1):
            chars[0].append(j)
        for j in range(1,len_s2+1):
            for i in range(1,len_s1+1):
                if string1[i-1] == string2[j-1]:
                    chars[i].insert(j, chars[i-1][j-1])
                else:
                    minimum = min(chars[i-1][j]+1, chars[i][j-1]+1, chars[i-1][j-1]+2)
                    chars[i].insert(j, minimum)
        dist = chars[-1][-1]

    return dist


with open("RefWords.txt", encoding="UTF-8-sig") as f:
    ref_words = f.read()
    ref_words = ref_words.split("\n")
with open("TestWords.txt", encoding="UTF-8-sig") as f:
    test_words = f.read()
    test_words = test_words.split("\n")
    test_words = test_words[:]


words = [ref_words, test_words]

dist = []

for i in range(len(words[1])):
    l = []
    for j in range(len(words[0])):
        distance = (words[0][j], words[1][i], Mylevenshtein(words[1][i], words[0][j]))
        l.append(distance)
    dist.append(l)

for i in range(len(dist)):
    suggested_word = min(dist[i], key=operator.itemgetter(2))

with open("SuggestedWords.txt", "+w", encoding="UTF-8") as f:
    for i in range(len(dist)):
        suggested_word = min(dist[i], key=operator.itemgetter(2))
        ind = dist[i].index(suggested_word)
        words = ""
        for j in range(len(dist[i][ind])-1):
            words += str(dist[i][ind][j]) + "\t"
        f.write(words)
        f.write("\n")


print(dist)
with open("MyLevenshtein.txt", "w+", encoding="UTF-8") as f:
    f.write("\t")
    for i in range(len(test_words)):
        f.write(test_words[i])
        f.write("\t")
    f.write("\n")
    for i in range(len(ref_words)):
        f.write("{:<15}".format(ref_words[i]))
        f.write("\t")
        for j in range(len(test_words)):
            f.write("{:<9}".format(str(dist[j][i][2])))
            f.write("\t")
        f.write("\n")
