import LA
puntuators = [';', ',', '\n', ':', '[', ']', '{', '}', '(', ')']

operators = ['and', 'or', 'not', '*', '/', '%', '+', '-', '<',
             '>', '>=', '<=', '!=', '==', 'band', 'bor', 'bnot', 'bxor', '.']

assignments = ['+=', '-=', '*=', '/=', '%=', '=']

seperators = []
seperators.extend(puntuators)
seperators.extend(operators)
seperators.extend(assignments)

dot = '.'
space = ' '
quotes = ['"', "'"]
Opencmt = '/*'
Closecmt = '*/'
cmts = [Opencmt, Closecmt]


def BreakWord(string):
    lexeme = ''
    res = []
    i = 0
    dotcount = 0
    while (i < len(string)):
        char = string[i]
        if(char == '/' and string[i+1] == '*'):
            char += string[i+1]
            i += 1
        if char in cmts:
            cmtIp = char
            if i == len(string):
                break
            lexeme += char
            i += 1
            char = string[i]
            while(Closecmt not in lexeme):
                lexeme += char
                if i == len(string)-1:
                    break
                i += 1
                char = string[i]
            if(i == len(string)):
                res.append(lexeme)
                lexeme = ''
                break
            char = string[i]
            res.append(lexeme)
            lexeme = ''
        if char in quotes:
            qouteIp = char
            if char == '\n':
                break
            lexeme += char
            i += 1
            char = string[i]
            while(char != qouteIp):
                if char == '\n':
                    break
                lexeme += char
                i += 1
                char = string[i]
            #lexeme += char
            #i += 1
            if(char == '\n'):
                res.append(lexeme)
                lexeme = ''
                # break
            # char = string[i]
            # res.append(lexeme)
            # lexeme = ''
        if char != space:
            lexeme += char
        if i == len(string)-1:
            if char == space or char in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
            else:
                res.append(lexeme)
                lexeme = ''
        if (i+1 < len(string)):
            nextch = string[i+1]
            prech = string[i-1]

            if(nextch == '=')and(char in seperators):
                lexeme += nextch
                i += 1
            if(nextch == dot):
                dotcount += 1
                i += 1
                char = string[i]
                nextch = string[i+1]
                if(LA.isAlpha(nextch) or len(lexeme) != 1 or nextch in seperators):
                    res.append(lexeme)
                    lexeme = ''
                if(dotcount > 0):
                    lexeme += char
                    #i += 1
                # elif(dotcount > 1):
                 #   res.append(lexeme)
                 #   lexeme = ''
            if string[i+1] == space or string[i+1] in seperators or lexeme in seperators:
                if(char == '+'or char == '-'):
                    if(prech == '=' or prech == space or prech in operators):
                        if(string[i+1] != space):
                            i = i+1
                            char = string[i]
                            lexeme += char
                            while(char not in seperators and string[i+1] not in seperators and string[i+1] != space):
                                i = i+1
                                char = string[i]
                                lexeme += char
                if ((lexeme != '') and (dot not in lexeme)):
                    res.append(lexeme)
                    lexeme = ''
            if(nextch == ';' and lexeme):
                res.append(lexeme)
                lexeme = ''
            if char == dot and len(lexeme) == 1 and LA.isAlpha(nextch):
                res.append(lexeme)
                lexeme = ''
        i = i+1
    return res


'''
def BreakWord(string):
    lexeme = ''
    res = []
    i = 0
    while (i < len(string)):
        char = string[i]
        if(char == '/' and string[i+1] == '*'):
            char += string[i+1]
            i += 1
        if char in cmts:
            cmtIp = char
            if i == len(string):
                break
            lexeme += char
            i += 1
            char = string[i]
            while(Closecmt not in lexeme):
                lexeme += char
                if i == len(string)-1:
                    break
                i += 1
                char = string[i]
            #lexeme += char
            #i += 1
            if(i == len(string)):
                res.append(lexeme)
                lexeme = ''
                break
            char = string[i]
            res.append(lexeme)
            lexeme = ''
        if char in quotes:
            qouteIp = char
            if i == len(string):
                break
            lexeme += char
            i += 1
            char = string[i]
            while(char != qouteIp):
                lexeme += char
                if i == len(string)-1:
                    break
                i += 1
                char = string[i]
            lexeme += char
            i += 1
            if(i == len(string)):
                res.append(lexeme)
                lexeme = ''
                break
            char = string[i]
            res.append(lexeme)
            lexeme = ''
        if char != space:
            lexeme += char
        if i == len(string)-1:
            if char == space or char in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
        if (i+1 < len(string)):
            nextch = string[i+1]
            prech = string[i-1]
            if(nextch == '=')and(char in seperators):
                lexeme += nextch
                i += 1
            if string[i+1] == space or string[i+1] in seperators or lexeme in seperators:
                if(char == '+'or char == '-'):
                    if(prech == '=' or prech == space or prech in operators):
                        if(string[i+1] != space):
                            i = i+1
                            char = string[i]
                            lexeme += char
                            while(char not in seperators and string[i+1] not in seperators and string[i+1] != space):
                                i = i+1
                                char = string[i]
                                lexeme += char
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
        i = i+1
    return res
'''

'''
def BreakWord(string):
    lexeme = ''
    res = []
    i = 0
    dotcount = 0
    while (i < len(string)):
        char = string[i]
        if(char == '/' and string[i+1] == '*'):
            char += string[i+1]
            i += 1
        if char in cmts:
            cmtIp = char
            if i == len(string):
                break
            lexeme += char
            i += 1
            char = string[i]
            while(Closecmt not in lexeme):
                lexeme += char
                if i == len(string)-1:
                    break
                i += 1
                char = string[i]
            if(i == len(string)):
                res.append(lexeme)
                lexeme = ''
                break
            char = string[i]
            res.append(lexeme)
            lexeme = ''
        if char in quotes:
            qouteIp = char
            if i == len(string):
                break
            lexeme += char
            i += 1
            char = string[i]
            while(char != qouteIp):
                lexeme += char
                if i == len(string)-1:
                    break
                i += 1
                char = string[i]
            lexeme += char
            i += 1
            if(i == len(string)):
                res.append(lexeme)
                lexeme = ''
                break
            char = string[i]
            res.append(lexeme)
            lexeme = ''
        if char != space:
            lexeme += char
        if i == len(string)-1:
            if char == space or char in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
            else:
                res.append(lexeme)
                lexeme = ''
        if (i+1 < len(string)):
            nextch = string[i+1]
            prech = string[i-1]

            if(nextch == '=')and(char in seperators):
                lexeme += nextch
                i += 1
            if(nextch == dot):
                dotcount += 1
                i += 1
                char = string[i]
                nextch = string[i+1]
                if(LA.isAlpha(nextch) or len(lexeme) != 1):
                    res.append(lexeme)
                    lexeme = ''
                if(dotcount > 0):
                    lexeme += char
                    #i += 1
                # elif(dotcount > 1):
                 #   res.append(lexeme)
                 #   lexeme = ''
            if string[i+1] == space or string[i+1] in seperators or lexeme in seperators:
                if(char == '+'or char == '-'):
                    if(prech == '=' or prech == space or prech in operators):
                        if(string[i+1] != space):
                            i = i+1
                            char = string[i]
                            lexeme += char
                            while(char not in seperators and string[i+1] not in seperators and string[i+1] != space):
                                i = i+1
                                char = string[i]
                                lexeme += char
                if lexeme != '' and dot not in lexeme:
                    res.append(lexeme)
                    lexeme = ''
            if char == dot and len(lexeme) == 1 and LA.isAlpha(nextch):
                res.append(lexeme)
                lexeme = ''
        i = i+1
    return res
'''

'''
def BreakWord(string):
    lexeme = ''
    res = []
    i = 0
    while (i < len(string)):
        char = string[i]
        if char in quotes:
            qouteIp = char
            if i == len(string):
                break
            lexeme += char
            i += 1
            char = string[i]
            while(char != qouteIp):
                lexeme += char
                if i == len(string)-1:
                    break
                i += 1
                char = string[i]
            lexeme += char
            i += 1
            if(i == len(string)):
                res.append(lexeme)
                break
            char = string[i]
            res.append(lexeme)
            lexeme = ''
        if char != space:
            lexeme += char
        if i == len(string)-1:
            if char == space or char in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
        if (i+1 < len(string)):
            nextch = string[i+1]
            if(nextch == '=')and(char in seperators):
                lexeme += nextch
                i += 1
            if string[i+1] == space or string[i+1] in seperators or lexeme in seperators:
                if(char == '+'or char == '-'):
                    prech = string[i-1]
                    if(prech == '=' or prech == space):
                        if(string[i+1] != space):
                            i = i+1
                            char = string[i]
                            lexeme += char
                            while(char not in seperators and string[i+1] not in seperators and string[i+1] != space):
                                i = i+1
                                char = string[i]
                                lexeme += char
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
        i = i+1
    return res
'''

'''
def BreakWord(string):
    lexeme = ''
    res = []
    i = 0
    while (i < len(string)):
        char = string[i]
        if char in quotes:
            qouteIp = char
            if i == len(string):
                break
            lexeme += char
            i += 1
            char = string[i]
            while(char != qouteIp):
                lexeme += char
                if i == len(string)-1:
                    break
                i += 1
                char = string[i]
            lexeme += char
            i += 1
            char = string[i]
            res.append(lexeme)
            lexeme = ''
        if char != space:
            lexeme += char
        if i == len(string)-1:
            if char == space or char in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
        if (i+1 < len(string)):
            nextch = string[i+1]
            if(nextch == '=')and(char in seperators):
                lexeme += nextch
                i += 1
            if string[i+1] == space or string[i+1] in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
        i = i+1
    return res
'''

'''def my_split(s):
    res = [s]
    for sep in seperators:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    while(''in res):
        res.remove('')
    return res
'''
