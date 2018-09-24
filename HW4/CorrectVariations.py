import re
import importlib.util
spec = importlib.util.spec_from_file_location("CombineFiles", "CombineFiles.py")
HW1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(HW1)


def CorrectVariations(path, InTextFilename, TableVariations):
    with open(TableVariations, encoding="UTF8") as f:
        variations = f.read().split("\n")
        list_variations = list(variations)[1:]
        variations = [i.split("\t") for i in list_variations]
    # Open the file to be corrected.
    with open(path + InTextFilename, encoding="UTF-8") as g:
        t = g.read()
    # Apply the variations.
    for i in range(len(variations)):
        pat = re.compile(variations[i][0])
        t = re.sub(pat, variations[i][1], t)

    with open(path+"ZebraAllNormalized.txt", "w+", encoding="UTF8") as f:
        f.write(t)
    return t
