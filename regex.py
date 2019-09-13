import re


KW = ['for', 'while', 'in', 'if', 'else', 'elif', 'break', 'cont', 'true', 'false',
      'class', 'public', 'private', 'protected', 'sealed', 'virtual', 'override',
      'overload', 'def', 'mul', 'dict', 'void', 'return', 'var', 'int', 'float',
      'char', 'string', 'bool', 'main', 'tuple', 'and', 'or', 'not', 'band', 'bor', 'bnot', 'bxor']


def isKw(str1):
    if str1 in KW:
        return str1
    return ""


def isIdentifier(str1):
    pattern = re.compile(r"(^[^\d\W]\w*\Z)")
    if(re.fullmatch(pattern, str1)):
        # print('ID')
        return True


def isIntConstant(str1):
    pattern = re.compile(r"([+|-][0-9]+)|([0-9]+)")
    if(re.fullmatch(pattern, str1)):
        #print('Int Constant')
        return True


def isFloatConstant(str1):
    pattern = re.compile(r"([+|-][0-9]*[.][0-9]+)|([0-9]*[.][0-9]+)")
    if(re.fullmatch(pattern, str1)):
        #print('Float Constant')
        return True


def isCharConstant(str1):
    pattern = re.compile(r"[\w\W]")
    if(re.fullmatch(pattern, str1)):
        #print('Char Constant')
        return True


def isStringConstant(str1):
    pattern = re.compile(r"[\w\W]*")
    if(re.fullmatch(pattern, str1)):
        #print('String Constant')
        return True


# isIdentifier('_a_')
# isIntConstant('+92')
# isFloatConstant('-.3')
# isCharConstant('#')
# isStringConstant("a")
