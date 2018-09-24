import re
import importlib.util
spec = importlib.util.spec_from_file_location("CombineFiles", "CombineFiles.py")
HW1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(HW1)


def CorrectVariations(InTextFilename, TableVariations):
    with open(TableVariations, encoding="UTF8") as f:
        variations = f.read().split("\n")
        list_variations = list(variations)[1:]
        variations = [i.split("\t") for i in list_variations]
    # Open the file to be corrected.کارگروهیان
    with open(InTextFilename, encoding="UTF-8") as g:
        t = g.read()
    # Apply the variations.
    for i in range(len(variations)):
        pat = re.compile(variations[i][0])
        t = re.sub(pat, variations[i][1], t)
    return t
with open("ZebraAllNormalized.txt", "w", encoding="UTF8") as f:
    f.write(CorrectVariations("ZebraAllCoding.txt", "TableVariations.txt"))

#Write the final stats to a file.
stats = HW1.CountWordsFile("ZebraAllNormalized.txt")
with open("StatsZebraAllNormalized.txt", "a", encoding="UTF8") as f:
    f.write("Number of all words: " + str(stats[0]))
    f.write("\n")
    f.write("Number of unique words: " + str(stats[1]))
    f.write("\n")
    f.write("Word Frequencies: ")
    f.write("\n")
    for i in range(len(stats[2])):
        f.write(str(stats[2][i]))
        f.write("\n")
