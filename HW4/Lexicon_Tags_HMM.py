import re

lexicon = {}
tags = {}
with open("POST-Persian-Corpus-Train.txt", encoding="UTF8") as f:
    train = f.read()
    train = re.sub(r"              *", "\t", train)
    train = train.split("\n")


with open("POST-Persian-Corpus-Test.txt", encoding="UTF-8") as f:
    test = f.read()
    test = re.sub(r"              *", "\t", test)
    test = test.split("\n")

text = train + test
for item in text:
    item = item.split("\t")
    lexicon[item[0]] = lexicon.get(item[0], 0) + 1
    tags[item[1]] = tags.get(item[1], 0) + 1

with open("Lexicon.txt", "w+", encoding="UTF8") as f:
    for word in lexicon:
        f.write(word+"\n")
with open("Tags.txt", "w+", encoding="UTF8") as f:
    for tag in tags:
        f.write(tag+"\n")


with open("POST-Persian-Corpus-Test.txt", encoding="UTF8") as f:
    text = f.read()
    text = re.sub(r"              *", "~", text)

    text = text.split("\n")
    test_words = []
    test_tags = []
    for item in text:
        item = item.split("~")
        test_words.append(item[0])
        test_tags.append(item[1])

with open("POST-Persian-Corpus-Test-Sent.txt","w+", encoding="UTF8") as f:
    for word in test_words:
        f.write(word + "\n")
