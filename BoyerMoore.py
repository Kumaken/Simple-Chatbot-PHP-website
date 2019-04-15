def BuildLast(pattern) :
    last = [-1]*128
    for i in range (0,len(pattern)):
        last[ord(pattern[i])] = i

    return last

def BoyerMooreMatching (text,pattern) :
    last = BuildLast(pattern)
    n = len(text)
    m = len(pattern)
    i = m - 1 
    if (i > n-1) :
        return -1    

    j = m - 1
    hit = 0
    temphit = 0
    check = 0
    while True :
        if(pattern[j] == text[i]):
            if (j==0) :
                hit = temphit + 1
                check = check + 1
                return hit/check
            else :
                check = check + 1
                temphit = temphit + 1
                i = i -1
                j = j - 1
        else :
            if(temphit >= hit ):
                hit = temphit
                temphit = 0
            lo = last[ord(text[i])]
            i = i + m - min(j,1+lo)
            j = m-1
        if (i > n-1) :
            break
    return -1

##Test Program
text = "AzharDhiaulhaq"
pattern = "Dhia"
posn = BoyerMooreMatching(text,pattern)
if (posn == -1) :
    print("Pattern not found")
else :
    print("Persentase : ", posn*100)