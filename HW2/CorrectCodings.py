def CorrectCoding(InTextFilename, TableCodings):
    ''' Returns the text with correct, unified coding.
    Input: InTextFilename(str), TableCodings(str)
    Output: normalized_text (str)
    '''
    #Open the file containing the codings and remove '\ufeff' character.
    with open(TableCodings, encoding="UTF-8") as f:
        content = f.read().split("\n")
        list_content = list(content)[1:]
        codings = [i.split("\t") for i in list_content]

    #Open the file to be corrected.
    with open(InTextFilename, encoding="UTF-8") as g:
        t = g.read()

    normalized_t = ""
    #Two lists of correct and incorrect encodings.
    inc = [i[0] for i in codings]
    c = [i[1] for i in codings]

    #Correct the codings.
    for i in range(len(t)):
        if t[i] in inc:
            ind = inc.index(t[i])
            normalized_t += c[ind]
        else:
            normalized_t += t[i]

    #Write the result to a file.
    with open("ZebraAllCoding.txt", "w", encoding = "UTF8") as g:
        g.write(normalized_t)

    return normalized_t

with open("ZebraAllCoding.txt", "w", encoding="UTF8") as f:
    f.write(CorrectCoding("ZebraAllPuncs.txt", "TableCodings.txt"))
