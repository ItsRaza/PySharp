
puntuators = [';', ',', '\n', ':', '[', ']', '{', '}', '(', ')', '.']

operators = ['and', 'or', 'not', '*', '/', '%', '+', '-', '<',
             '>', '>=', '<=', '!=', '==', 'band', 'bor', 'bnot', 'bxor']

assignments = ['+=', '-=', '*=', '/=', '%=', '=']

seperators = []
seperators.extend(puntuators)
seperators.extend(operators)
seperators.extend(assignments)


space = ' '
quotes = ['"', "'"]


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


'''def my_split(s):
    res = [s]
    for sep in seperators:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    while(''in res):
        res.remove('')
    return res


    def lex(string):
    lexeme = ''
    res = []
    for i, char in enumerate(string):
        if char != space:
            lexeme += char  # adding a char each time
        if (i+1 < len(string)):  # prevents error
            # if next char == ' '
            if string[i+1] == space or string[i+1] in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    print(lexeme.replace('\n', 'newline'))
                    lexeme = ''
    return res
'''

'''def BreakWord(string):
    lexeme = ''
    res = []
    i = 0
    while (i < len(string)):
        char = string[i]
        if char in quotes:
            if i == len(string):
                break
            i += 1
            check = string[i]
            while(check != char):
                lexeme += check
                if i == len(string)-1:
                    break
                i += 1
                check = string[i]
            res.append(lexeme)
            lexeme = ''
            if check == char:
                i += 1
                char = string[i]
        if char != space:
            lexeme += char
        if i == len(string)-1:
            if char == space or char in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
        if (i+1 < len(string)):
            nextch = string[i+1]
            if(nextch == '='):
                lexeme += nextch
                i += 1
            if string[i+1] == space or string[i+1] in seperators or lexeme in seperators:
                if lexeme != '':
                    res.append(lexeme)
                    lexeme = ''
        i = i+1
    return res'''
