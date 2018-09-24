import re
import string
import operator
import os
from glob import glob
import importlib

def Normalizer(text):
    purified_text = ""
    # Replace all half-spaces more than with with one half-space.
    re.sub(r"\u200c{2,}", "\u200c", text)
    # Replace all latin characters with a space.
    latin = re.compile(r"[A-Za-z]")
    latinfree_text = re.sub(latin, " ", text)
    # Put spaces between numbers.
    pat1 = re.compile(r"(.+)([0-9]+)")
    re.sub(pat1, "\1 \2", text)
    pat2 = re.compile(r"([0-9])(.+)")
    re.sub(pat2,"\1 \2", text)
    # Remove Farsi-specific punctuation marks.
    punc = ["(", "[", "“", "«", "{", ")", "\]", "”", "»","!", ",", ";", "؛", ":", "،", "؟"]
    for p in punc:
        f_pat = re.compile(r'[' + p + ']')
        latinfree_text = re.sub(f_pat, " ", latinfree_text)

    # Replace all punctuation marks left, available in the string module.
    for char in latinfree_text:
        if char not in string.punctuation:
            purified_text += char
        else:
            purified_text += " "

    #Replace all spaces more than one with only one space.
    normalized_text = ' '.join(purified_text.split())
    return normalized_text

def CountWordsFile(TextFilename):

    ''' Returns the number of words in a text.
    Input : name of the file (str) It's the address.
    Output : number of all words, all unique words and the repetition of each unique word (int)
    '''
    with open(TextFilename,"r", encoding="utf-8") as file:
        text = file.read()
    t = Normalizer(text)

    #Find the number of words.
    no_words = len(t.split(' '))
    #Find the frequency of each unique word.
    freq = {}
    for word in t.split(' '):
        freq[word] = freq.get(word, 0) + 1

    no_unique_words = len(freq)
    #Sort the frequencies in a descending order.
    sorted_freq = sorted(freq.items(), key=operator.itemgetter(1))
    sorted_freq.reverse()
    return (no_words, no_unique_words, sorted_freq)

def FindFiles(path):
    '''
    Return all files in a path.
    Input: a path (str)
    Output: paths to all the files in the given path. (list)
    '''
    result = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.txt'))]
    return result

def CountWordsFolder(Path):
    '''Returns the result of CountWordsFile over a folder path, for each folder and for the Zebra corpus.
    Input : path (str)
    Output: Number of all words and unique words for the given folder and for Zebra.
    '''
    p = []
    Folders = os.listdir(Path)
    SumAll, SumUnique = 0, 0
    FolderAll, FolderUnique = [], []
    #Obtain the path for each subfolder and put it in a list.
    for Folder in Folders:
        p.append(os.path.join(Path + "\\" + str(Folder)))
    #For each subfolder, find all the .txt files, get the result and put it in a list.
    for i in range(len(p)):
        f = FindFiles(p[i])
        for j in range(len(f)):
            SumAll += CountWordsFile(f[j])[0]
            SumUnique += CountWordsFile(f[j])[1]
        FolderAll.append((Folders[i], SumAll))
        FolderUnique.append((Folders[i], SumUnique))
    #Calculate the result for the whole corpus.
    ZebraAll = sum([x[1] for x in FolderAll])
    ZebraUnique = sum([x[1] for x in FolderUnique])
    return ZebraAll, ZebraUnique, FolderUnique

def CombineFiles(Path, x):
    '''Returns the content of files in a folder each in one line. Each line represents the conent of one .txt file in
    the folder.
    Input: path (str)
    Output: text(str)
    '''
    train_outfile, test_outfile = "", ""
    paths = FindFiles(Path)

    Paths = []
    for i in range(0, len(paths), 10):
        Paths.append(paths[i : i+10])


    P = []
    for path in Paths:
        t = ""
        for i in range(x):
            with open(path[i], "r", encoding="utf-8") as h:
                t += h.read().replace("\n", "")
        P.append(t)


    for file in range(len(P)):
        train_outfile = train_outfile + P[file] + "\n"

    P = []
    for path in Paths:
        t = ""
        for i in range(x, len(path)):
            with open(path[i], "r", encoding="utf-8") as h:
                t += h.read().replace("\n", "")
        P.append(t)

    for file in range(len(P)):
        test_outfile = test_outfile + P[file] + "\n"

    return train_outfile, test_outfile
