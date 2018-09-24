import re
#Import the modules from HW1.
import importlib.util
c = importlib.util.spec_from_file_location("CountChar", "E:\CL\Semester2\IntrotoCL\HW\HW2\CountChar.py")
HW2 = importlib.util.module_from_spec(c)
c.loader.exec_module(HW2)


def CorrectPuncs(path, Filename):
    ''' Returns a text correctly punctuated.
    Input: path (str)
    Output: t4 (str)
    '''
    with open(path+Filename, encoding= "UTF8") as f:
        t = f.read()

    P1 = "\(\[“«{"
    P2 = "\)\]”»}"
    P3 = "؟،:؛;!,."

    pat1 = re.compile(r"(.)?([" + P1 +  "])(.)?")
    t1 = re.sub(pat1,r"\1 \2\3", t)

    pat2 = re.compile(r"(.)?([" + P2 +  "])(.)?")
    t2 = re.sub(pat2, r"\1\2 \3", t1)

    pat3 = re.compile(r"(.)?([" + P3 +  "])(.)?")
    t3 = re.sub(pat3, r"\1\2 \3", t2)

    pat4 = re.compile(r"(.)?([" + P1 +"])( )+(.)?")
    t4 = re.sub(pat4, r"\1\2\4", t3)

    pat5 = re.compile(r"(.)?( )+([" + P2 + P3 +"])(.)?")
    t5 = re.sub(pat5, r"\1\3\4", t4)

    pat6 = re.compile(r"(\.)( )(\.\.)")
    t6 = re.sub(pat6, r"\1\3", t5)

    pat7 = re.compile(r"(\.\.\.)(.)+?(\w)")
    t7 = re.sub(pat7, r"\1\2 \3", t6)

    pat8 = re.compile(r" +")
    t8 = re.sub(pat8, " ", t7)

    pat9 = re.compile(r"([" + P2 + P1 +"])" + "( )([" + P3 + "])")
    t9 = re.sub(pat9, r"\1\3", t8)

    with open(path + "ZebraAllPuncs.txt", "w+", encoding="UTF8") as f:
        f.write(t9)

    return t9

