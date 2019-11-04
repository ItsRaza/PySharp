# import regex
# import WordSplitter
import LA

GI = 0


def SST(TKs):
    SST_sel = ['ID', 'this', 'while', 'if', 'for', 'return',
               'static', 'DT', 'tuple', 'dict', 'ID', 'var']
    if(TKs[GI].CP in SST_sel):
        #GI += 1
        if(NewDec(TKs)):
            return True
        elif (NewAssignSt(TKs)):
            return True
        elif (WhileSt(TKs)):
            return True
        elif (IfElseSt(TKs)):
            return True
        elif (ForSt(TKs)):
            return True
        elif (NewIncDecSt(TKs)):
            return True
        elif (RetSt(TKs)):
            return True
        elif (FnCall(TKs)):
            return True
        else:
            return False


def MST(TKs):
    MST_sel = ['ID', 'this', 'while', 'if', 'for', 'return']
    if(TKs[GI].CP in MST_sel):
        #GI += 1
        if(SST(TKs)):
            if(MST(TKs)):
                return True
    else:
        return False


def StaticOp(TKs):
    global GI
    StaticOp_sel = ['static', 'DT', 'tuple', 'ID', 'var']
    if(TKs[GI].CP in StaticOp_sel):
        if(TKs[GI].CP == 'static'):
            GI += 1
            return True
        return True
    else:
        return False


def RetTypes(TKs):
    RetTypes_sel = ['DT', 'tuple', 'dict', 'ID', 'var', 'void']
    if(TKs[GI].CP in RetTypes_sel):
        if(ToDec(TKs)):
            return True
        elif(TKs[GI].CP == 'void'):
            GI += 1
            return True
    else:
        return False


def PL(TKs):
    PL_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')']
    if(TKs[GI].CP in PL_sel):
        #GI += 1
        if(PLOpts2(TKs)):
            if(TKs[GI].CP == ','):
                GI += 1
                return True
    return False


def Body(TKs):
    Body_sel = [';', '{', 'ID', 'this', 'while', 'if', 'for', 'return']
    if(TKs[GI].CP == ':' in Body_sel):
        if(TKs[GI].CP == ';'):
            GI += 1
        if(SST(TKs)):
            return True
        elif(TKs[GI].CP == '{'):
            GI += 1
            if(MST(TKs)):
                if(TKs[GI].CP == '}'):
                    GI += 1
                    return True

    else:
        return False


def FnDec(TKs):
    global GI
    if(TKs[GI].CP == 'def'):
        GI += 1
        if(StaticOp(Tks)):
            if(RetTypes(Tks)):
                if(TKs[GI].CP == 'ID'):
                    GI += 1
                    if(TKs[+GI].CP == '('):
                        GI += 1
                        if(PL(Tks)):
                            GI += 1
                            if(TKs[GI].CP == ')'):
                                if(Body(Tks)):
                                    return True
    return False


def ClassTypesL(TKs):
    ClassTypesL_sel = ['AM', 'static', 'abstract', 'class']
    if(TKs[GI].CP in ClassTypesL_sel):
        if(ClassTypes(TKs)):
            if(ClassTypesL(TKs)):
                return True
    return True


def Inheri(Tks):
    if(TKs[GI].CP == ':' or TKs[GI].CP == '{'):
        if(TKs[GI].CP == ':'):
            GI += 1
            if(InheriOPts(TKs)):
                return True
    else:
        return False


def ClassBody(TKs):
    if(TKs[GI].CP == '{'):
        GI += 1
        if(ClassBodyL(TKs)):
            if(TKs[GI].CP == '}'):
                GI += 1
                return True
    else:
        return False


def ClassDec(TKs):
    global GI
    ClassDec_sel = ['AM', 'class', 'static', 'abstract']
    if(TKs[GI].CP in ClassDec_sel):
        #GI += 1
        if(ClassTypesL(TKs)):
            if(TKs[GI].CP == 'class'):
                GI += 1
                if(TKs[GI].CP == 'ID'):
                    GI += 1
                    if(Inheri(TKs)):
                        if(ClassBody(TKs)):
                            return True
    else:
        return False


def ToDec(TKs):
    global GI
    ToDec_sel = ['tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in ToDec_sel):
        GI += 1
        return True


def FactorID2(TKs):
    return True


def FactorBraces(TKs):
    return True


def OE(TKs):
    return True


def FIOpts(TKs):
    global GI
    print(GI)
    FIOpts_sel = ['AOP', '(', '[', '.']
    if(TKs[GI].CP in FIOpts_sel):
        #GI += 1
        if(IncDecOp()):
            if(OE(TKs)):
                return True
        elif(TKs[GI].CP == '('):
            GI += 1
            if(FactorBraces(TKs)):
                if(TKs[GI].CP == ')'):
                    GI += 1
                    return True
        elif FactorID2(TKs):
            return True
    else:
        return False


def FactorID(TKs):
    global GI
    if(TKs[GI].CP == 'ID'):
        GI += 1
        print(GI)
        if(FIOpts(TKs)):
            return True
    return False


def Dec(TKs):
    Dec_sel = ['static', 'tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in Dec_sel):
        if(StaticOp(TKs)):
            if(ToDec(TKs)):
                if(FactorID(TKs)):
                    return True
    return False


def NewDec(TKs):
    global GI
    NewDec_sel = ['static', 'tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in NewDec_sel):
        if(Dec(TKs)):
            if(TKs[GI].CP == ';'):
                GI += 1
                return True
    else:
        return False


def GlobalDefs(TKs):
    GlobalDefs_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var']
    print(TKs[GI].CP)
    if(TKs[GI].CP in GlobalDefs_sel):
        if(NewDec(TKs)):
            if(GlobalDefs(TKs)):
                return True
    else:
        return False


def Defs(TKs):
    Defs_sel = ['def', 'AM', 'static', 'abstract', 'class',
                'DT', 'tuple', 'dict', 'ID', 'var', 'main', '$']
    if(TKs[GI].CP in Defs_sel):
        print(GI)
        if(FnDec(TKs)):
            if(Defs(TKs)):
                return True
        elif(ClassDec(TKs)):
            if(Defs(TKs)):
                return True
        elif(GlobalDefs(TKs)):
            if(Defs(TKs)):
                return True
        else:
            return False
    else:
        return False


def Start(TKs):
    global GI
    GI = 0
    Start_sel = ['def', 'public', 'private', 'protected', 'sealed', 'static',
                 'abstract', 'class', 'DT', 'tuple', 'dict', 'ID', 'var']
    if(TKs[GI].CP in Start_sel):
        print(GI)
        if(Defs(TKs)):
            if(TKs[GI].CP == 'main'):
                GI += 1
                if(TKs[GI].CP == '('):
                    GI += 1
                    if(TKs[GI].CP == ')'):
                        GI += 1
                        if(TKs[GI].CP == '{'):
                            GI += 1
                            if(MST(TKs)):
                                if(TKs[GI].CP == '}'):
                                    GI += 1
                                    if(Defs(TKs)):
                                        return True
    else:
        return False


def SA(TKs):
    if(Start(TKs)):
        print("Start")


'''
def SST(TKs, GI):
    SST_sel = ['ID', 'this', 'while', 'if', 'for', 'return',
               'static', 'DT', 'tuple', 'dict', 'ID', 'var']
    if(TKs[GI].CP in SST_sel):
        #GI += 1
        if(NewDec(TKs, GI)):
            return True
        elif (NewAssignSt(TKs, GI)):
            return True
        elif (WhileSt(TKs, GI)):
            return True
        elif (IfElseSt(TKs, GI)):
            return True
        elif (ForSt(TKs, GI)):
            return True
        elif (NewIncDecSt(TKs, GI)):
            return True
        elif (RetSt(TKs, GI)):
            return True
        elif (FnCall(TKs, GI)):
            return True
        else:
            return False


def MST(TKs, GI):
    MST_sel = ['ID', 'this', 'while', 'if', 'for', 'return']
    if(TKs[GI].CP in MST_sel):
        #GI += 1
        if(SST(TKs, GI)):
            if(MST(TKs, GI)):
                return True
    else:
        return False


def StaticOp(TKs, GI):
    StaticOp_sel = ['static', 'DT', 'tuple', 'ID', 'var']
    if(TKs[GI].CP in StaticOp_sel):
        #GI += 1
        return True
    else:
        return False


def RetTypes(TKs, GI):
    RetTypes_sel = ['DT', 'tuple', 'dict', 'ID', 'var', 'void']
    if(TKs[GI].CP in RetTypes_sel):
        #GI += 1
        return True
    else:
        return False


def PL(TKs, GI):
    PL_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')']
    if(TKs[GI].CP in PL_sel):
        #GI += 1
        if(PLOpts2(TKs, GI)):
            if(TKs[GI].CP == ','):
                GI += 1
                return True
    return False


def Body(TKs, GI):
    Body_sel = [';', '{', 'ID', 'this', 'while', 'if', 'for', 'return']
    if(TKs[GI].CP in Body_sel):
        #GI += 1
        if(SST(TKs, GI)):
            return True
        elif(TKs[GI].CP == '{'):
            GI += 1
            if(MST(TKs, GI)):
                if(TKs[GI].CP == '}'):
                    GI += 1
                    return True

    else:
        return False


def FnDec(TKs, GI):
    if(TKs[GI].CP == 'def'):
        GI += 1
        if(StaticOp(Tks, GI)):
            if(RetTypes(Tks, GI)):
                if(TKs[GI].CP == 'ID'):
                    GI += 1
                    if(TKs[GI].CP == '('):
                        GI += 1
                        if(PL(Tks, GI)):
                            GI += 1
                            if(TKs[GI].CP == ')'):
                                if(Body(Tks, GI)):
                                    return True
    return False


def ClassTypesL(TKs, GI):
    ClassTypesL_sel = ['AM', 'static', 'abstract', 'class']
    if(TKs[GI].CP in ClassTypesL_sel):
        if(ClassTypes(TKs, GI)):
            if(ClassTypesL):
                return True
    return False


def Inheri(Tks, GI):
    if(TKs[GI].CP == ':' or TKs[GI].CP == '{'):
        GI += 1
        if(InheriOPts()):
            return True


def ClassBody(TKs, GI):
    if(TKs[GI].CP == '{'):
        GI += 1
        if(ClassBody2(TKs, GI)):
            if(TKs[GI].CP == '}'):
                GI += 1
    else:
        return False


def ClassDec(TKs, GI):
    ClassDec_sel = ['AM', 'class', 'static', 'abstract']
    if(TKs[GI].CP in ClassDec_sel):
        #GI += 1
        if(ClassTypesL(TKs, GI)):
            if(TKs[GI].CP == 'class'):
                GI += 1
                if(TKs[GI].CP == 'ID'):
                    GI += 1
                    if(Inheri(TKs, GI)):
                        if(ClassBody(TKs, GI)):
                            return True
    else:
        return False


def ToDec(TKs, GI):
    ToDec_sel = ['tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in ToDec_sel):
        GI += 1
        return True


def FactorID2(TKs, GI):
    return True


def FactorBraces(TKs, GI):
    return True


def OE(TKs, GI):
    return True


def FIOpts(TKs, GI):
    FIOpts_sel = ['AOP', '(', '[', '.']
    if(TKs[GI].CP in FIOpts_sel):
        #GI += 1
        if(OE(TKs, GI)):
            return True
        elif(FactorBraces(TKs, GI)):
            if(TKs[GI].CP == ')'):
                GI += 1
                return True
        elif FactorID2(TKs, GI):
            return True
    else:
        False


def FactorID(TKs, GI):
    if(TKs[GI].CP == 'ID'):
        GI += 1
        if(FIOpts(TKs, GI)):
            return True
    return False


def Dec(TKs, GI):
    Dec_sel = ['static', 'tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in Dec_sel):
        #GI += 1
        if(StaticOp(TKs, GI)):
            if(ToDec(TKs, GI)):
                if(FactorID(TKs, GI)):
                    return True
    return False


def NewDec(TKs, GI):
    NewDec_sel = ['static', 'tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in NewDec_sel):

        if(Dec(TKs, GI)):
            return True
    else:
        return False


def GlobalDefs(TKs, GI):
    GlobalDefs_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var']
    print(TKs[GI].CP)
    if(TKs[GI].CP in GlobalDefs_sel):
        if(NewDec(TKs, GI)):
            if(GlobalDefs(Tks, GI)):
                return True
    else:
        return False


def Defs(TKs, GI):
    Defs_sel = ['def', 'AM', 'static', 'abstract', 'class',
                'DT', 'tuple', 'dict', 'ID', 'var', 'main', '$']
    if(TKs[GI].CP in Defs_sel):
        print(GI)
        if(FnDec(TKs, GI)):
            if(Defs(TKs, GI)):
                return True
        elif(ClassDec(TKs, GI)):
            if(Defs(TKs, GI)):
                return True
        elif(GlobalDefs(TKs, GI)):
            if(Defs(TKs, GI)):
                return True
        else:
            return False
    else:
        return False


def Start(TKs, GI):
    Start_sel = ['def', 'public', 'private', 'protected', 'sealed', 'static',
                 'abstract', 'class', 'DT', 'tuple', 'dict', 'ID', 'var']
    if(TKs[GI].CP in Start_sel):
        print(GI)
        if(Defs(TKs, GI)):
            if(TKs[GI].CP == 'main'):
                GI += 1
                if(TKs[GI].CP == '('):
                    GI += 1
                    if(TKs[GI].CP == ')'):
                        GI += 1
                        if(TKs[GI].CP == '{'):
                            GI += 1
                            if(MST(TKs, GI)):
                                if(TKs[GI].CP == '}'):
                                    GI += 1
                                    if(Defs(TKs, GI)):
                                        return True
    else:
        return False


def SA(TKs):
    global GI
    if(Start(TKs, GI)):
        print("Start")
'''
