def CountChar(path, char):
    ''' Returns the number of a character in a text file, given the path.
    Input: path(str), char (str)
    Output: i(int)
    '''
    with open(path, "r", encoding= "UTF-8") as f:
        t = f.read()
    i = 0
    for l in t:
        if l == char:
            i += 1
    return i
