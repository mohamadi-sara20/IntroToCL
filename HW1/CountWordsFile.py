import re
import string
import operator
import os
from glob import glob

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
    with open("FarsiPunctuation.txt", encoding="utf-8") as file:
        f_punc = file.read()
    f_pat = re.compile(r'[' + f_punc + ']')
    clean_text = re.sub(f_pat, " ", latinfree_text)
    # Replace all punctuation marks left, available in the string module.
    for char in clean_text:
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
