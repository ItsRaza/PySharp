# import regex
# import WordSplitter
import LA

GI = 0


def NewAssignSt(TKs):
    global GI
    NewAssignSt_sel = ['ID', 'this']
    if(TKs[GI].CP in NewAssignSt_sel):
        if(AssignSt(TKs)):
            if(TKs[GI].CP == ';'):
                GI += 1
                return True
    else:
        return False


def WhileSt(TKs):
    global GI
    if(TKs[GI].CP == 'while'):
        GI += 1
        if(TKs[GI].CP == '('):
            GI += 1
            if(OE(TKs)):
                if(TKs[GI].CP == ')'):
                    GI += 1
                    if(Body(TKs)):
                        return True
    else:
        return False


def IfElseOpts(TKs):
    global GI
    IfElseOpts_sel = ['ID', 'this', 'while',
        'if', 'for', 'return', 'else', 'elif']
    if(TKs[GI].CP in IfElseOpts_sel):
        if(TKs[GI].CP == 'else'):
            GI += 1
            if(Body(TKs)):
                return True
        elif(TKs[GI].CP == 'elif'):
            GI += 1
            if(TKs[GI].CP == '('):
                GI += 1
                if(OE(TKs)):
                    if(TKs[GI].CP == ')'):
                        GI += 1
                        if(Body(TKs)):
                            if(IfElseOpts(TKs)):
                                return True

        return True
    else:
        return False


def IfElseSt(TKs):
    global GI
    if(TKs[GI].CP == 'if'):
        GI += 1
        if(TKs[GI].CP == '('):
            GI += 1
            if(OE(TKs)):
                if(TKs[GI].CP == ')'):
                    GI += 1
                    if(Body(TKs)):
                        if(IfElseOpts(TKs)):
                            return True
    else:
        return False


def C1(TKs):
    global GI
    C1_sel = ['this', 'static', 'DT', 'tuple',
        'dict', 'ID', 'var', 'not', 'True', 'False',';']
    if(TKs[GI].CP in C1_sel):
        if(NewDec(TKs)):
            return True
        elif(NewAssignSt(TKs)):
            return True
        elif (TKs[GI].CP==';'):
            GI+=1
            return True
        return True
    else:
        return False


def C2(TKs):
    global GI
    C2_sel = ['ID', 'IntConst', 'FloatConst',
        'CharConst', 'StringConst', '(', 'True', 'False',';']
    print(GI)
    if(TKs[GI].CP in C2_sel):
        if(OE(TKs)):
            return True
        # elif (TKs[GI].CP==';'):
        #     GI+=1
        #     return True
        return True
    else:
        return False


def C3(TKs):
    global GI
    C3_sel = ['ID', 'this', ')']
    if(TKs[GI].CP in C3_sel):
        if(AssignSt(TKs)):
            return True
        elif(NewIncDecSt(TKs)):
            return True
        return True
    else:
        return False


def NewIncDecSt(TKs):
    global GI
    if(TKs[GI].CP == 'ID'):
        if(IncDec(TKs)):
            if(TKs[GI].CP == ','):
                GI += 1
                return True
            return True
    else:
        return False

def IncDec(TKs):
    global GI
    if(TKs[GI].CP=='ID'):
        if(FactorID(TKs)):
            return True
    else:
        return False       


def ForOpts(TKs):
    global GI
    if(TKs[GI].CP=='(' or TKs[GI].CP=='ID'):
        if(TKs[GI].CP=='('):
            GI+=1
            if(C1(TKs)):
                if(C2(TKs)):
                    if(TKs[GI].CP==';'):
                        GI+=1
                        if(C3(TKs)):
                            if(TKs[GI].CP==')'):
                                GI+=1
                                return True
        elif(TKs[GI].CP=='ID'):
            GI+=1
            if(TKs[GI].CP=='in'):
                if(OE(TKs)):
                    return True
    else:
        return False

def ForSt(TKs):
    global GI
    if(TKs[GI].CP=='for'):
        GI+=1
        if(ForOpts(TKs)):
            if(Body(TKs)):
                return True
    else:
        return False

def RetSt(TKs):
    global GI
    if(TKs[GI].CP=='return'):
        GI+=1
        if(OE(TKs)):
            if(TKs[GI].CP==';'):
                GI+=1
                return True
    else:
        return False

def SST(TKs):
    global GI
    SST_sel = ['ID', 'this', 'while', 'if', 'for', 'return',
               'static', 'DT', 'tuple', 'dict', 'ID', 'var']
    print(GI)
    if(TKs[GI].CP in SST_sel):
        # GI += 1
        if(NewAssignSt(TKs)):
            return True
        elif (NewDec(TKs)):
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
    global GI
    MST_sel = ['ID', 'this', 'while', 'if', 'for', 'return','DT']
    if(TKs[GI].CP in MST_sel):
        # GI += 1
        if(SST(TKs)):
            if(MST(TKs)):
                return True
        return True
    else:
        return False


def StaticOp(TKs):
    global GI
    StaticOp_sel = ['static', 'DT', 'tuple', 'ID', 'var','void']
    if(TKs[GI].CP in StaticOp_sel):
        if(TKs[GI].CP == 'static'):
            GI += 1
        return True
    else:
        return False



def RetTypes(TKs):
    global GI
    RetTypes_sel = ['DT', 'tuple', 'dict', 'ID', 'var', 'void']
    if(TKs[GI].CP in RetTypes_sel):
        if(TKs[GI].CP=='ID'):
            return True
        if(ToDec(TKs)):
            return True
        elif(TKs[GI].CP == 'void'):
            GI += 1
            return True
    else:
        return False

def AssignSt(TKs):
    global GI
    AssignSt_sel=['ID','this']
    if(TKs[GI].CP in AssignSt_sel):
        if(FactorID(TKs)):
            return True
        elif(Tks[GI].Cp=='this'):
            GI+=1
            if(x(TKs)):
                if(Init(TKs)):
                    if(OEL(TKs)):
                        return True
    else:
        return False

def PLOpts(TKs):
    global GI
    PLOpts_sel=['static','DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in PLOpts_sel):
        if(Dec(TKs)):
            return True
        elif (OE(TKs)):
            return True
        elif(AssignSt(TKs)):
            return True
    else:
        return False
    
def PLOpts2(TKs):
    global GI
    PLOpts2_sel=['static','DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in PLOpts2_sel):
        if(PLOpts(TKs)):
            if(PL(TKs)):
                return True
            return True
    else:
        return False


def PL(TKs):
    global GI
    PL_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')']
    if(TKs[GI].CP in PL_sel):
        if(PLOpts2(TKs)):
            if(TKs[GI].CP == ','):
                GI += 1
                return True
        if(TKs[GI].CP==')'):
            return True
    return False


def Body(TKs):
    global GI
    Body_sel = [';', '{', 'ID', 'this', 'while', 'if', 'for', 'return']
    if(TKs[GI].CP in Body_sel):
        if(TKs[GI].CP == ';'):
            GI += 1
        elif(SST(TKs)):
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
        if(StaticOp(TKs)):
            if(RetTypes(TKs)):
                if(TKs[GI].CP == 'ID'):
                    GI += 1
                    if(TKs[+GI].CP == '('):
                        GI += 1
                        if(PL(TKs)):
                            # GI += 1
                            if(TKs[GI].CP == ')'):
                                GI+=1
                                if(Body(TKs)):
                                    return True
    return False

def ClassTypes(TKs):
    global GI
    ClassTypes_sel=['AM','static','abstract']
    if(TKs[GI].CP=='AM' or TKs[GI].CP=='static' or TKs[GI].CP=='abstract'):
        GI+=1
        return True

def ClassTypesL(TKs):
    global GI
    ClassTypesL_sel = ['AM', 'static', 'abstract', 'class']
    if(TKs[GI].CP in ClassTypesL_sel):
        if(ClassTypes(TKs)):
            if(ClassTypesL(TKs)):
                return True
        return True
    return False

def InheriOPts(TKs):
    global GI
    InheriOPts_sel=['ID','mul']
    if(TKs[GI].CP in InheriOPts_sel):
        if(TKs[GI].CP=='ID'):
            GI+=1
            return True
        elif(TKs[GI].CP=='mul'):
            GI+=1
            if(TKs[GI].CP=='('):
                GI+=1
                if(TKs[GI].CP=='ID'):
                    GI+=1
                    if(TKs[GI].CP==','):
                        GI+=1
                        if(TKs[GI].CP=='ID'):
                            GI+=1
                            if(TKs[GI].CP==')'):
                                GI+=1
                                return True
    else:
        return False

def Inheri(TKs):
    global GI
    if(TKs[GI].CP == ':' or TKs[GI].CP == '{'):
        if(TKs[GI].CP == ':'):
            GI += 1
            if(InheriOPts(TKs)):
                return True
        return True
    else:
        return False

def FnInheri(TKs):
    global GI
    FnInheri_sel=[':','{','ID','this','while','if','for','return','AM','VO']
    if(TKs[GI].CP in FnInheri_sel):
        if(TKs[GI].CP==':'):
            GI+=1
            if(FnCall(TKs)):
                return True
        return True
    else:
        return False

def Constructor(TKs):
    global GI
    if(TKs[GI].CP=='ID'):
        if(FactorID(TKs)):
            if(Body(TKs)):
                return True
    else:
        return False

def ClassBodyOpts2(TKs):
    global GI
    ClassBodyOpts2_sel=['AM','VO','ID','DT','def']
    if(TKs[GI].CP in ClassBodyOpts2_sel):
        if(FnDec(TKs)):
            if(FnInheri(TKs)):
                if(Body(TKs)):
                    return True
        elif (NewDec(TKs)):
            return True
        elif (Constructor(TKs)):
            return True
    else:
        return False

def AMVO(TKs):
    global GI
    if(TKs[GI].CP=='AM' or TKs[GI].CP=='VO'):
        GI+=1
        return True

def AMVOL(TKs):
    global GI
    AMVOL_sel=['AM','VO']
    if(TKs[GI].CP in AMVOL_sel):
        if(AMVO(TKs)):
            if(AMVOL(TKs)):
                return True
        return True
    else:
        return False

def ClassBodyOpts(TKs):
    global GI
    ClassBodyOpts_sel=['AM','VO']
    if(TKs[GI].CP in ClassBodyOpts_sel):
        if(TKs[GI].CP=='AM'):
            GI+=1
            if(TKs[GI].CP==':'):
                GI+=1
                if(ClassBodyOpts2(TKs)):
                    if(ClassBodyOpts(TKs)):
                        return True
                    return True
        elif(AMVOL(TKs)):
            if(ClassBodyOpts2(TKs)):
                return True
    else:
        return False


def ClassBodyL(TKs):
    global GI
    ClassBodyL_sel=['AM','VO','}']
    if(TKs[GI].CP in ClassBodyL_sel):
        if(ClassBodyOpts(TKs)):
            return True
        return True
    else:
        return False

def ClassBody(TKs):
    global GI
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
        # GI += 1
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
        print(GI)
        return True
    return False


def xOpts(TKs):
    global GI
    xOpts_sel=['IntConst','AOP']
    if(TKs[GI].CP in xOpts_sel):
        if(TKs[GI].CP=='IntConst'):
            GI+=1
            if(FactorComma(TKs)):
                if(xOpts(TKs)):
                    return True
                return True
        return True
    else:
        return False

def Slice(TKs):
    global GI
    if(TKs[GI].CP=='IntConst'):
        GI+=1
        if(TKs[GI].CP==':'):
            GI+=1
            if(TKs[GI].CP=='IntConst'):
                return True
    else:
        return False

def FactorBrackets(TKs):
    global GI
    FactorBrackets_sel=['IntConst',']']
    if(TKs[GI].CP in FactorBrackets_sel):
        if(xOpts(TKs)):
            return True
        elif(Slice(TKs)):
            return True
    else:
        return False

def xOpts2(TKs):
    global GI
    xOpts2_sel=['ID','[','.','AOP']
    if(TKs[GI].CP in xOpts2_sel):
        if(FactorID(TKs)):
            return True
        elif(x(TKs)):
            return True
    else:
        return False

def x(TKs):
    global GI
    x_sel=['[','.','AOP',',']
    if(TKs[GI].CP in x_sel):
        if(TKs[GI].CP=='['):
            GI+=1
            if(FactorBrackets(TKs)):
                if(TKs[GI].CP==']'):
                    GI+=1
                    if(x(TKs)):
                        return True
        elif(TKs[GI].CP=='.'):
            GI+=1
            if(xOpts2(TKs)):
                return True     
        return True
    else:
        return False

def StuffDic(TKs):
    global GI
    StuffDic_sel=['ID', 'IntConst','FloatConst', 'CharConst', 'StringConst','(', 'not', 'True', 'False',':']
    if(TKs[GI].CP in StuffDic_sel):
        if(OE(TKs)):
            return True
        return True
    else:
        return False

def MoreDic(TKs):
    global GI
    MoreDic_sel=[',','}']
    if(TKs[GI].CP in MoreDic):
        if(TKs[GI].CP==','):
            GI+=1
            if(Dic(TKs)):
                return True
        return True
    else:
        return False

def Dic(TKs):
    global GI
    Dic_sel=['ID', 'IntConst','FloatConst', 'CharConst', 'StringConst','(', 'not', 'True', 'False',':']
    if(TKs[GI].CP in Dic_sel):
        if(OE(TKs)):
            return True
        elif(StuffDic(TKs)):
            if(TKs[GI].CP==':'):
                GI+=1
                if(StuffDic(TKs)):
                    if(MoreDic(TKs)):
                        return True
        return True
    else:
        return False

def TupleDec(TKs):
    global GI
    if(TK[GI].CP=='('):
        GI+=1
        if(OEL(TKs)):
            if(TK[GI].CP==')'):
                return True
    else:
        return False

def InitOpts(TKs):
    global GI
    InitOpts_sel=['ID', 'IntConst','FloatConst', 'CharConst', 'StringConst', '(','{','[','this', 'not', 'True', 'False']
    if(TKs[GI].CP in InitOpts_sel):
        if(FactorID(TKs)):
            return True
        elif (OE(TKs)):
            return True
        elif(TKs[GI].CP=='new'):
            GI+=1
            if(TKs[GI].CP=='ID'):
                GI+=1
                if(TKs[GI].CP=='('):
                    GI+=1
                    if(FactorBraces(TKs)):
                        if(TKs[GI].CP==')'):
                            GI+=1
                            return True
        elif(Init(TKs)):
            return True
        elif(TKs[GI].CP=='{'):
            GI+=1
            if(Dic(TKs)):
                if(TKs[GI].CP=='}'):
                    Gi+=1
                    return True
        elif(TupleDec(TKs)):
            return True
        elif(TKs[GI].CP=='['):
            GI+=1
            if(OEL(TKs)):
                if(TKs[GI].CP==']'):
                    GI+=1
                    return True
        elif(TKs[GI].CP=='this'):
            if(x(TKs)):
                return True
    else:
        return False

def Init(TKs):
    global GI
    Init_sel=['ID', 'IntConst',
             'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False','AOP',',']
    if(TKs[GI].CP in Init_sel):
        if(TKs[GI].CP=='AOP'):
            GI+=1
            if(InitOpts(TKs)):
                return True
        return True
    else:
        return False



def FI2Opts(TKs):
    global GI
    FI2Opts_sel=['ID', 'IntConst',
             'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False','static','DT','tuple','dict','var','this',',']
    if(TKs[GI].CP in FI2Opts_sel):
        if(OEL2(TKs)):
            return True
    else:
        return False

def FactorID2(TKs):
    global GI
    FactorID2_sel = ['[', '.','AOP',',']
    if(TKs[GI].CP in FactorID2_sel):
        if(x(TKs)):
            if(Init(TKs)):
                if(FI2Opts(TKs)):
                    return True
    else:
        return False

# def FCOptsL(TKs):
#     global GI
#     FCOptsL_sel=['AOP','ID','IntConst','FloatConst','CharConst','StringConst','not','(','True','False']
#     if(TKs[GI].CP in FCOptsL_sel):
#         if(Init(TKs)):
#             if(OEL(TKs)):
#                 return True
#         elif(OE(TKs)):
#             if(OEL2(TKs)):
#                 return True

def FCOpts(TKs):
    global GI
    FCOptsL_sel=['static','DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in FCOptsL_sel):
        if(OEL(TKs)):
            return True
    return False

def FactorComma(TKs):
    global GI
    if(TKs[GI].CP==','):
        if(TKs[GI].CP==','):
            GI+=1
            if(FCOpts(TKs)):
                return True
        return True
    else:
        return False

def OEL2(TKs):
    global GI
    if(TKs[GI].CP==','):
        if(FactorComma(TKs)):
            return True
        return True
    else:
        return False

def OEL(TKs):
    global GI
    OEL_sel=['ID', 'IntConst',
             'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in OEL_sel):
        if(OE(TKs)):
            if(OEL2(TKs)):
                return True
        return True
    else:
        return False

def FactorBraces(TKs):
    global GI
    FactorBraces_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
                        'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')']
    if(TKs[GI].CP in FactorBraces_sel):
        if(OEL(TKs)):
            return True
        elif (PL(TKs)):
            return True
        return True
    else:
        return False

def FnCall(TKs):
    global GI
    if(TKs[GI].CP=='ID'):
        if(FactorID(TKs)):
            return True
    else:
        return False    



def T(TKs):
    global GI
    T_sel = ['ID', 'IntConst',
             'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in T_sel):
        if(FactorID(TKs)):
            if(OE(TKs)):
                return True
            return True
        elif(TKs[GI].CP=='IntConst' or TKs[GI].CP=='FloatConst' or TKs[GI].CP=='CharConst' or TKs[GI].CP=='StringConst'):
            GI+=1
            return True
        elif(FnCall(TKs)):
            return True
        elif(TKs[GI].CP=='('):
            GI+=1
            if(FnCall(TKs)):
                if(TKs[GI].CP==')'):
                    GI+=1
                    return True
        elif(TKs[GI].CP=='not'):
            GI+=1
            if(T(TKs)):
                return True
        elif(IncDec(TKs)):
            return True
        elif(TKs[GI].CP=='True'):
            return True
        elif(TKs[GI].CP=='False'):
            return True

def NT_(TKs):
    global GI
    NT__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')', ':', 'or', 'and', 'ROP', 'PM','MDM',';']
    if(TKs[GI].CP in NT__sel):
        if(TKs[GI].CP == 'MDM'):
            GI += 1
            if(T(TKs)):
                if(NT_(TKs)):
                    return True
        return True
    else:
        return False

def NT(TKs):
    global GI
    NT_sel = ['ID', 'IntConst',
             'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in NT_sel):
        if(T(TKs)):
            if(NT_(TKs)):
                return True
    else:
        return False

def E_(TKs):
    global GI
    E__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')', ':', 'or', 'and', 'ROP', 'PM',';']
    if(TKs[GI].CP in E__sel):
        if(TKs[GI].CP == 'PM'):
            GI += 1
            if(NT(TKs)):
                if(E_(TKs)):
                    return True
        return True
    else:
        return False


def E(TKs):
    global GI
    E_sel = ['ID', 'IntConst',
             'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in E_sel):
        if(NT(TKs)):
            if(E_(TKs)):
                return True
    else:
        return False


def RE_(TKs):
    global GI
    RE__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
               'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')', ':', 'or', 'and', 'ROP',';']
    if(TKs[GI].CP in RE__sel):
        if(TKs[GI].CP == 'ROP'):
            GI += 1
            if(E(TKs)):
                if(RE_(TKs)):
                    return True
        return True
    else:
        return False


def RE(TKs):
    global GI
    RE_sel = ['ID', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in RE_sel):
        if(E(TKs)):
            if(RE_(TKs)):
                return True
    else:
        return False


def AE_(TKs):
    global GI
    AE__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
               'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')', ':', 'or', 'and',';']
    if(TKs[GI].CP in AE__sel):
        if(TKs[GI].CP == 'and'):
            GI += 1
            if(RE(TKs)):
                if(AE_(TKs)):
                    return True
        return True
    else:
        return False


def AE(TKs):
    global GI
    AE_sel = ['ID', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in AE_sel):
        if(RE(TKs)):
            if(AE_(TKs)):
                return True
    else:
        return False


def OE_(TKs):
    global GI
    OE__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'IntConst',
               'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False', ',', ')', ':', 'or',';']
    if(TKs[GI].CP in OE__sel):
        if(TKs[GI].CP == 'or'):
            GI += 1
            if(AE(TKs)):
                if(OE_(TKs)):
                    return True
        return True
    else:
        return False


def OE(TKs):
    global GI
    OE_sel = ['ID', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in OE_sel):
        if(AE(TKs)):
            if(OE_(TKs)):
                return True
    else:
        return False


def IncDecOp(TKs):
    global GI
    if(TKs[GI].CP == 'AOP'):
        GI += 1
        return True


def FIOpts(TKs):
    global GI
    print(GI)
    FIOpts_sel = ['AOP', '(', '[', '.',',','ID', 'IntConst',
              'FloatConst', 'CharConst', 'StringConst', '(', 'not', 'True', 'False',';',')','ROP']
    if(TKs[GI].CP in FIOpts_sel):
        # GI += 1
        if(IncDecOp(TKs)):
            if(OE(TKs)):
                return True
            if(x(TKs)):
                return True
        if(TKs[GI].CP=='ROP'):
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
        elif(OE(TKs)):
            return True
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
    global GI
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
    global GI
    GlobalDefs_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var']
    print(TKs[GI].CP)
    if(TKs[GI].CP in GlobalDefs_sel):
        if(NewDec(TKs)):
            if(GlobalDefs(TKs)):
                return True
            return True
    else:
        return False

def BodyOpts(TKs):
    global GI
    BodyOpts_sel=[';','{','ID','this','while','if','for','return','def',
                'AM','static','abstract','class','DT','tuple','dict','ID','var','main','$']
    if(TKs[GI].CP in BodyOpts_sel):
        if(Body(TKs)):
            return True
        return True
    else:
        return False

def FnDec2(TKs):
    global GI
    if(TKs[GI].CP=='def'):
        if(FnDec(TKs)):
            if(BodyOpts(TKs)):
                return True
    else:
        return False

def Defs(TKs):
    global GI
    Defs_sel = ['def', 'AM', 'static', 'abstract', 'class',
                'DT', 'tuple', 'dict', 'ID', 'var', 'main', '$']
    if(TKs[GI].CP in Defs_sel):
        print(GI)
        if(FnDec2(TKs)):
            if(Defs(TKs)):
                return True
            return True
        elif(ClassDec(TKs)):
            if(Defs(TKs)):
                return True
            return True
        elif(GlobalDefs(TKs)):
            if(Defs(TKs)):
                return True
            return True
        elif (TKs[GI].CP=='main'):
            return True
        elif(TKs[GI].CP=='$'):
            return True
        # return True
    else:
        return False


def Start(TKs):
    global GI
    GI = 0
    Start_sel = ['def', 'public', 'private', 'protected', 'sealed', 'static',
                 'abstract', 'class', 'DT', 'tuple', 'dict', 'ID', 'var','main']
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
        # return True
    else:
        return False


def SA(TKs):
    global GI
    if(Start(TKs)):
        print("Valid Syntax")
    else:
        print("Syntax Error at Line Number ", TKs[GI].LineNo)
