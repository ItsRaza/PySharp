import regex
import WordSplitter
import Token
# import pickle

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

assignments = ['+=', '-=', '*=', '/=', '%=', '=']
MDM = ['*', '/', '%']
PM = ['+', '-']
ROP = ['<', '>', '>=', '<=', '!=', '==']
DT = ['int', 'float', 'char', 'double', 'string']
AM = ['public', 'private', 'protected', 'sealed']
VO = ['virtual', 'overide']


def lexer(filename):
    Tokens = []
    lineNo = 1
    string = readFile(filename)
    words = WordSplitter.BreakWord(string)
    print(len(words))
    print(words)
    for word in words:
        Token1 = Token.Token()
        if ('\n' in word):
            lineNo += 1
        if('/*' in word):
            pass
        if(word[0] == '_'):
            if(regex.isIdentifier(word)):
                Token1.CP = 'ID'
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
            else:
                Token1.CP = 'Invalid Lexeone'
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                # word = ""

        if(isAlpha(word[0])):
            if(regex.isIdentifier(word)):
                temp = regex.isKw(word)
                if(temp == ""):
                    Token1.CP = 'ID'
                    Token1.VP = word
                    Token1.LineNo = lineNo
                    Tokens.append(Token1)
                    # word = ""
                else:
                    Token1.VP = temp
                    if(temp in DT):
                        Token1.CP = 'DT'
                    elif(temp in AM):
                        Token1.CP = 'AM'
                    elif(temp in VO):
                        Token1.CP = 'VO'
                    else:
                        Token1.CP = temp
                        # Token1.VP = ""
                    Token1.LineNo = lineNo
                    Tokens.append(Token1)
                    # word = ""
            else:
                Token1.CP = 'Invalid Lexeone'
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                # word = ""
        if(word in WordSplitter.seperators):
            if(word == '\n'):
                #Token1.CP = "CharConst"
                #Token1.VP = "LineBreak"
                #Token1.LineNo = lineNo
                # Tokens.append(Token1)
                # word = ""
                pass
            else:
                Token1.VP = word
                if(word in assignments):
                    Token1.CP = "AOP"
                elif(word in MDM):
                    Token1.CP = "MDM"
                elif(word in PM):
                    Token1.CP = "PM"
                elif(word in ROP):
                    Token1.CP = "ROP"
                else:
                    Token1.CP = word
                    # Token1.VP = ""
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                # word = ""
        if(isDigit(word[0]) or ((word[0] == '+' or word[0] == '-') and (word not in WordSplitter.seperators))):
            if(regex.isIntConstant(word)):
                Token1.CP = "IntConst"
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                # word = ""
            elif(regex.isFloatConstant(word)):
                Token1.CP = "FloatConst"
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                # word = ""
            else:
                Token1.CP = 'Invalid Lexeone'
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                # word = ""
        if(word[0] in WordSplitter.quotes):
            if(regex.isStringConstant(word[1:-1])):
                if(len(word) == 3)or(len(word) == 4):
                    if(regex.isCharConstant(word[1:-1])):
                        Token1.CP = "CharConst"
                        Token1.VP = word[1:-1]
                        Token1.LineNo = lineNo
                        Tokens.append(Token1)
                        # word = ""
                else:
                    Token1.CP = "StringConst"
                    Token1.VP = word[1:-1]
                    Token1.LineNo = lineNo
                    Tokens.append(Token1)
                    # word = ""
    Token11 = Token.Token()
    Token11.CP = "$"
    Token11.VP = '$'
    Token11.LineNo = lineNo
    Tokens.append(Token11)
    return Tokens


def readFile(filename):
    with open(filename, 'r') as myfile:
        data = myfile.read()
    return data


def isAlpha(ch):
    if((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')):
        if(ch in WordSplitter.puntuators):
            return False
        return True


def isDigit(ch):
    if(ch in digits):
        return True


'''
def lexer(filename):
    Tokens = []
    lineNo = 0
    string = readFile(filename)
    words = WordSplitter.BreakWord(string)
    i = 0
    while (i <= len(words)):
        word = words[i]
        Token1 = Token.Token()
        if (word[0] == '\n'):
            lineNo += 1
        if(word[0] == '_'):
            if(regex.isIdentifier(word)):
                Token1.CP = 'ID'
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]
            else:
                Token1.CP = 'Invalid Lexeone'
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]

        if(isAlpha(word[0])):
            if(regex.isIdentifier(word)):
                temp = regex.isKw(word)
                if(temp == ""):
                    Token1.CP = 'ID'
                    Token1.VP = word
                    Token1.LineNo = lineNo
                    Tokens.append(Token1)
                    i += 1
                    word = words[i]
                else:
                    Token1.CP = temp
                    Token1.LineNo = lineNo
                    Tokens.append(Token1)
                    i += 1
                    word = words[i]
            else:
                Token1.CP = 'Invalid Lexeone'
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]
        if(word in WordSplitter.seperators):
            if(word == '\n'):
                Token1.CP = "CharConst"
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]
            else:
                Token1.CP = word
                Token1.VP = ""
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]
        if(isDigit(word[0])):
            if(regex.isIntConstant(word)):
                Token1.CP = "IntConst"
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]
            elif(regex.isFloatConstant(word)):
                Token1.CP = "FloatConst"
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]
            else:
                Token1.CP = 'Invalid Lexeone'
                Token1.VP = word
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]
        if(word[0] in WordSplitter.quotes):
            if(len(word) == 3)or(len(word) == 4):
                if(regex.isCharConstant(word[1:-1])):
                    Token1.CP = "CharConst"
                    Token1.VP = word[1:-1]
                    Token1.LineNo = lineNo
                    Tokens.append(Token1)
                    i += 1
                    word = words[i]
            if(regex.isStringConstant(word)):
                Token1.CP = "StringConst"
                Token1.VP = word[1:-1]
                Token1.LineNo = lineNo
                Tokens.append(Token1)
                i += 1
                word = words[i]
    return Tokens
'''
