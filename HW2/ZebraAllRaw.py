import importlib.util
spec = importlib.util.spec_from_file_location("CombineFiles", "CombineFiles.py")
HW1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(HW1)

#Merge all files into one.
ZebraAllRaw = HW1.CombineFiles("MergedFolders")
with open("ZebraAllRaw.txt", "w", encoding= "UTF-8") as f:
    f.write(ZebraAllRaw)

#Use CountWordsFile function, get the stats and put it into a file.
stats = HW1.CountWordsFile("ZebraAllRaw.txt")
print(stats)
#Write the result to a file.
with open("StatsZebraAllRaw.txt", "a", encoding="UTF8") as f:
    f.write("Number of all words: " + str(stats[0]))
    f.write("\n")
    f.write("Number of unique words: " + str(stats[1]))
    f.write("\n")
    f.write("Word Frequencies: ")
    f.write("\n")
    for i in range(len(stats[2])):
        f.write(str(stats[2][i]))
        f.write("\n")
