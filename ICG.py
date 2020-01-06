import LA
import ClassTable
import SymbolTable
import ClassDataTable
import regex
import WordSplitter

CLSTBL=ClassTable.ClassTable()
SYMTBL=SymbolTable.SymbolTable()
stack=[]


GI = 0
stack_Scope = []
Scope_no    = 0 
L=0
Tt=0
def CreatLable():
    global L
    L+=1
    return 'L'+str(L)

def CreatTemp():
    global Tt
    Tt+=1
    return 'T'+str(Tt)

def CreateScope():
    global Scope_no
    stack_Scope.append(Scope_no)
    Scope_no += 1
    return (Scope_no - 1)

def DestroyScope():
    s=stack_Scope.pop()
    if(stack_Scope != None):
        return s
    else:
        return -1

def FnLookup(N,para,CN,AM,TM,S,gbl):
    if(CN!=''and gbl!=False):
        T=CLSTBL.LookupCDT(CN,N,AM,TM)
        if(T==''):
            T=SYMTBL.FnLookupST(N,S)
        # return T
    elif(CN!='' and gbl==False):
        T=CLSTBL.LookupCDT(CN,N,AM,TM)
        # return T
    elif(CN==''):
        T=SYMTBL.FnLookupST(N,S)
        if(T!=para):
            T=''
        # return T
    if(T=='' or T== None):
        return False
    else:
        return T

def Compatibility(LT,RT,op):
    rT=''
    if(op=='or' or op=='and'):
        rT='bool'
        return rT
    if(op=='==' or op=='!=' or op=='>=' or op=='<=' or op=='<'or op=='>'):
        rT='bool'
        return rT
    if(op=='=' or op=='+=' or op=='-=' or op=='*=' or op=='/='):
        if(LT==RT):
            return LT
    if(op=='.'):
        if(regex.isIdentifier(LT)):
            rT=RT
            return rT
    if((LT=='int' and RT=='int') or (RT=='int' and LT=='int')):
        if(op=='*' or op=='/' or op=='-' or op=='+'):
            rT='int'
            return rT
    if((LT=='int' and RT=='float') or (RT=='int' and LT=='float')):
        if(op=='*' or op=='/' or op=='-' or op=='+'):
            rT='float'
            return rT
    if((LT=='string' and RT=='string')):
        if(op=='+'):
            rT='string'
            return rT
    if((LT=='char' and RT=='char')):
        if(op=='+'):
            rT='char'
            return rT
    
        
def NewAssignSt(TKs,CN,AM,T,TM,S):
    global GI
    NewAssignSt_sel = ['ID', 'this']
    if(TKs[GI].CP in NewAssignSt_sel):
        T=AssignSt(TKs,CN,AM,T,TM,S)
        if(T):
            if(TKs[GI].CP == ';'):
                GI += 1
                return T
    else:
        return False


def WhileSt(TKs,CN,AM,T,TM,S):
    global GI
    if(TKs[GI].CP == 'while'):
        L1=CreatLable()
        with open('IC.txt','a') as f:
            f.write(L1+':')
            f.write('\n')
        GI += 1
        if(TKs[GI].CP == '('):
            GI += 1
            S=CreateScope()
            T=OE(TKs,CN,AM,T,TM,S)
            if(T):
                if(TKs[GI].CP == ')'):
                    L2=CreatLable()
                    with open('IC.txt','a') as f:
                        f.write('if('+T+'==false) jmp '+L2)
                        f.write('\n')
                    GI += 1
                    if(Body(TKs,CN,AM,TM,S)):
                        with open('IC.txt','a') as f:
                            f.write('jmp '+L1)
                            f.write('\n')
                            f.write('jmp '+L2)
                            f.write('\n')
                        return True
    else:
        return False


def IfElseOpts(TKs,CN,AM,T,TM,S,*args):
    global GI
    L1=None
    if(len(args)>0):
        L1=args[0]
    IfElseOpts_sel = ['ID', 'this', 'while',
        'if', 'for', 'return', 'else', 'elif']
    if(TKs[GI].CP in IfElseOpts_sel):
        if(TKs[GI].CP == 'else'):
            L2=CreatLable()
            with open('IC.txt','a') as f:
                f.write('jmp '+L2)
                f.write('\n')
                f.write(L1+':')
            GI += 1
            if(Body(TKs,CN,AM,TM,S)):
                with open('IC.txt','a') as f:
                    f.write(L2+':')
                    f.write('\n')
                return True
        elif(TKs[GI].CP == 'elif'):
            GI += 1
            if(TKs[GI].CP == '('):
                GI += 1
                S=CreateScope()
                T=OE(TKs,CN,AM,'',TM,S)
                if(T):
                    if(TKs[GI].CP == ')'):
                        GI += 1
                        if(Body(TKs,CN,AM,TM,S)):
                            if(IfElseOpts(TKs,CN,AM,T,TM,S)):
                                return True
        else:
            with open('IC.txt','a') as f:
                f.write(L1+':')
                f.write('\n')
            return True
    else:
        return False


def IfElseSt(TKs,CN,AM,T,TM,S):
    global GI
    if(TKs[GI].CP == 'if'):
        L1=CreatLable()
        GI += 1
        if(TKs[GI].CP == '('):
            GI += 1
            S=CreateScope()
            T=OE(TKs,CN,AM,'',TM,S)
            if(T):
                if(TKs[GI].CP == ')'):
                    with open('IC.txt','a') as f:
                        f.write('if('+T+'==false) jmp '+L1)
                        f.write('\n')
                    GI += 1
                    if(Body(TKs,CN,AM,TM,S)):
                        if(IfElseOpts(TKs,CN,AM,T,TM,S,L1)):
                            return True
    else:
        return False


def C1(TKs,CN,AM,T,TM,S):
    global GI
    C1_sel = ['this', 'static', 'DT', 'tuple',
        'dict', 'ID', 'var', 'not', 'True', 'False',';']
    if(TKs[GI].CP in C1_sel):
        if(NewDec(TKs,CN,AM,S)):
            return True
        elif(NewAssignSt(TKs,CN,AM,T,TM,S)):
            return True
        elif (TKs[GI].CP==';'):
            GI+=1
            return True
        return True
    else:
        return False


def C2(TKs,CN,AM,T,TM,S):
    global GI
    C2_sel = ['ID', 'int', 'float',
        'char', 'string', '(', 'True', 'False',';']
    print(GI)
    if(TKs[GI].CP in C2_sel):
        T=OE(TKs,CN,AM,'',TM,S)
        if(T):
            return T
        # elif (TKs[GI].CP==';'):
        #     GI+=1
        #     return True
        return T
    else:
        return False


def C3(TKs,CN,AM,T,TM,S):
    global GI
    C3_sel = ['ID', 'this', ')']
    if(TKs[GI].CP in C3_sel):
        T=AssignSt(TKs,CN,AM,T,TM,S)
        if(T): 
            return T
        elif(NewIncDecSt(TKs)):
            return True
        return True
    else:
        return False


def NewIncDecSt(TKs,CN,AM,TM,T,S):
    global GI
    if(TKs[GI].CP == 'ID'):
        if(IncDec(TKs,CN,AM,TM,T,S)):
            if(TKs[GI].CP == ','):
                GI += 1
                return True
            return True
    else:
        return False

def IncDec(TKs,CN,AM,TM,T,S):
    global GI
    if(TKs[GI].CP=='ID'):
        if(FactorID(TKs,CN,AM,TM,T,S)):
            return True
    else:
        return False       


def ForOpts(TKs,CN,AM,T,TM,S):
    global GI
    if(TKs[GI].CP=='(' or TKs[GI].CP=='ID'):
        if(TKs[GI].CP=='('):
            S=CreateScope()
            L1=CreatLable()
            L2=CreatLable()
            with open('IC.txt','a') as f:
                f.write(L1+':')
                f.write('\n')
            GI+=1
            T1=C1(TKs,CN,AM,T,TM,S)
            if(T1):
                T2=C2(TKs,CN,AM,T,TM,S)
                if(T2):
                    with open('IC.txt','a') as f:
                        f.write('if('+str(T2)+'==False) jmp '+L2)
                        f.write('\n')
                    if(TKs[GI].CP==';'):
                        GI+=1
                        T=C3(TKs,CN,AM,T,TM,S)
                        if(T):
                            if(TKs[GI].CP==')'):
                                GI+=1
                                return (L1,T,L2)
        elif(TKs[GI].CP=='ID'):
            GI+=1
            if(TKs[GI].CP=='in'):
                if(OE(TKs,CN,AM,T,TM,S)):
                    return True
    else:
        return False

def ForSt(TKs,CN,AM,T,TM,S):
    global GI
    if(TKs[GI].CP=='for'):
        GI+=1
        L1=ForOpts(TKs,CN,AM,T,TM,S)
        if(L1):
            if(Body(TKs,CN,AM,TM,S)):
                with open('IC.txt','a') as f:
                    f.write(str(L1[1])+'='+str(L1[1])+'+1')
                    f.write('\n')
                    f.write('jmp '+L1[0])
                    f.write('\n')   
                    f.write(L1[2]+':')
                    f.write('\n')
                return True
    else:
        return False

def RetSt(TKs,CN,AM,T,TM,S):
    global GI
    if(TKs[GI].CP=='return'):
        GI+=1
        if(OE(TKs,CN,AM,T,TM,S,0)):
            if(TKs[GI].CP==';'):
                GI+=1
                return True
    else:
        return False

def SST(TKs,CN,AM,TM,S):
    global GI
    # S=0
    # CN=''
    # AM=''
    # TM=''
    SST_sel = ['ID', 'this', 'while', 'if', 'for', 'return',
               'static', 'DT', 'tuple', 'dict', 'ID', 'var']
    print(GI)
    if(TKs[GI].CP in SST_sel):
        # GI += 1
        if(NewAssignSt(TKs,CN,AM,T,TM,S)):
            return True
        elif (NewDec(TKs,CN,AM,S)):
            return True
        elif (WhileSt(TKs,CN,AM,'',TM,S)):
            return True
        elif (IfElseSt(TKs,CN,AM,T,TM,S)):
            return True
        elif (ForSt(TKs,CN,AM,T,TM,S)):
            return True
        elif (NewIncDecSt(TKs,CN,AM,TM,T,S)):
            return True
        elif (RetSt(TKs,CN,AM,'',TM,S)):
            return True
        elif (FnCall(TKs,CN,AM,T,TM,S)):
            return True
        else:
            return False


def MST(TKs,CN,AM,TM,S):
    global GI
    MST_sel = ['ID', 'this', 'while', 'if', 'for', 'return','DT','}']
    if(TKs[GI].CP in MST_sel):
        # GI += 1
        if(SST(TKs,CN,AM,TM,S)):
            if(MST(TKs,CN,AM,TM,S)):
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
            return 'static'
        return None
    else:
        return False



def RetTypes(TKs):
    global GI
    RetTypes_sel = ['DT', 'tuple', 'dict', 'ID', 'var', 'void']
    if(TKs[GI].CP in RetTypes_sel):
        if(TKs[GI].CP=='ID'):
            GI+=1
            return TKs[GI-1].VP
        T=ToDec(TKs)  
        if(T):
            return T
        elif(TKs[GI].CP == 'void'):
            GI += 1
            return 'void'
    else:
        return False

def AssignSt(TKs, CN, AM, TM, T, S):
    global GI
    AssignSt_sel=['ID','this']
    if(TKs[GI].CP in AssignSt_sel):
        T=FactorID(TKs, CN, AM, TM, T, S)
        if(T):
            if(TKs[GI].VP=='('):
                GI+=1
                T1=FactorBraces(TKs,CN,AM,'',TM,S)
                T=T.split('-')[0]
                if(TKs[GI].VP==')'):
                    GI+=1
                    if(T1 == T):
                        return True
            elif(TKs[GI].VP in WordSplitter.assignments):
                if(Init(TKs,CN,AM,T,TM,S)):
                    return T
            return T
        elif(TKs[GI].CP=='this'):
            GI+=1
            if(x(TKs, CN, AM, TM, T, S)):
                if(Init(TKs, CN, AM, TM, T, S)):
                    if(OEL(TKs,CN,AM,T,TM,S)):
                        return True
    else:
        return False

def PLOpts(TKs,para,CN,AM,S,*args):
    global GI
    
    PLOpts_sel=['static','DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in PLOpts_sel):
        T=OE(TKs,CN,AM,'','',S,args[0])
        if(T=='' or T== None or T==False):
            T=Dec(TKs,CN,AM,S)
        if(T):
            para=para+T
            return para
        else:
            para='void'
            return para 
        # elif (OE(TKs)):
        #     return True
        # elif(AssignSt(TKs)):
        #     return True
    else:
        return False
    
def PLOpts2(TKs,para,CN,AM,S,*args):
    global GI
    # para=''
    PLOpts2_sel=['static','DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in PLOpts2_sel):
        para=PLOpts(TKs,para,CN,AM,S,args[0])
        if(para!=''):
            para=PL(TKs,para,CN,AM,S)
            if(para):
                return para
            return para
    else:
        return para


def PL(TKs,para,CN,AM,S,*args):
    global GI
    tem=None
    PL_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False', ',', ')']
    if(TKs[GI].CP in PL_sel):
        if(len(args)>0):
            tem=args[0]
        para=PLOpts2(TKs,para,'','',S,tem)
        if(para!=False):
            if(TKs[GI].CP==')'):
                return para
            if(TKs[GI].CP == ','):
                GI += 1
                return para
        if(TKs[GI].CP==')'):
            return para
    return False


def Body(TKs,CN,AM,TM,S):
    global GI
    Body_sel = [';', '{', 'ID', 'this', 'while', 'if', 'for', 'return']
    if(TKs[GI].CP in Body_sel):
        if(TKs[GI].CP == ';'):
            GI += 1
        elif(SST(TKs,CN,AM,TM,S)):
            return True
        elif(TKs[GI].CP == '{'):
            # S=CreateScope()
            GI += 1
            if(MST(TKs,CN,AM,TM,S)):
                if(TKs[GI].CP == '}'):
                    GI += 1
                    S=DestroyScope()
                    return True

    else:
        return False


def FnDec(TKs,CN,AM,TM,S):
    global GI
    Type=''
    if(TKs[GI].CP == 'def'):
        GI += 1
        TM=StaticOp(TKs)
        if(TM or TM==None):
            T=RetTypes(TKs)
            if(T):
                T=regex.isKw(T)
                if(T==''):
                    T=CLSTBL.LookupCT(T)
                    if(T==None):
                        print('No such Type exists ',T)
                        return False
                if(TKs[GI].CP == 'ID'):
                    N=TKs[GI].VP
                    GI += 1
                    if(TKs[+GI].CP == '('):
                        S=CreateScope()
                        GI += 1
                        para=PL(TKs,'',CN,AM,S,0)
                        
                        if(para!=False):
                            # GI += 1
                            if(TKs[GI].CP == ')'):
                                # S=DestroyScope()
                                Type=para+'->'+T
                                # Type=N+Type
                                t=FnLookup(N,para,CN,AM,TM,S,True)
                                if(t!=False):
                                    print('Function Redeclaration on ',TKs[GI].LineNo)
                                    return False
                                
                                if(CN!='' or AM!=''):
                                    CLSTBL.InsertCDT(CN,N,Type,AM,TM)
                                else:
                                    SYMTBL.InsertST(N,Type,S)
                                GI+=1
                                if(Body(TKs,'','',TM,S)):
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
    par=''
    InheriOPts_sel=['ID','mul']
    if(TKs[GI].CP in InheriOPts_sel):
        if(TKs[GI].CP=='ID'):
            N=TKs[GI].VP
            N=CLSTBL.LookupCT(N)
            if(N==None):
                print('ClassNotDeclared '+ TKs[GI].VP+' at line ',TKs[GI].LineNo)
                return False
            par=N
            GI+=1
            return par
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
            Par=InheriOPts(TKs)
            if(Par==False):
                return False
            if(Par):
                return Par
        return ''
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

def ClassBodyOpts2(TKs,CN,AM):
    global GI
    ClassBodyOpts2_sel=['AM','VO','ID','DT','def']
    if(TKs[GI].CP in ClassBodyOpts2_sel):
        if(FnDec(TKs,CN,AM,'',None)):
            if(FnInheri(TKs)):
                if(Body(TKs)):
                    return True
        elif (NewDec(TKs,CN,AM,0)):
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

def ClassBodyOpts(TKs,CN):
    global GI
    ClassBodyOpts_sel=['AM','VO']
    if(TKs[GI].CP in ClassBodyOpts_sel):
        if(TKs[GI].CP=='AM'):
            AM=TKs[GI].VP
            GI+=1
            if(TKs[GI].CP==':'):
                GI+=1
                if(ClassBodyOpts2(TKs,CN,AM)):
                    if(ClassBodyOpts(TKs,CN)):
                        return True
                    return True
        elif(AMVOL(TKs)):
            if(ClassBodyOpts2(TKs)):
                return True
    else:
        return False


def ClassBodyL(TKs,CN):
    global GI
    ClassBodyL_sel=['AM','VO','}']
    if(TKs[GI].CP in ClassBodyL_sel):
        if(ClassBodyOpts(TKs,CN)):
            return True
        return True
    else:
        return False

def ClassBody(TKs,CN):
    global GI
    if(TKs[GI].CP == '{'):
        GI += 1
        if(ClassBodyL(TKs,CN)):
            if(TKs[GI].CP == '}'):
                GI += 1
                return True
    else:
        return False


def ClassDec(TKs,S):
    global GI
    ClassDec_sel = ['AM', 'class', 'static', 'abstract']
    if(TKs[GI].CP in ClassDec_sel):
        # GI += 1
        if(ClassTypesL(TKs)):
            if(TKs[GI].CP == 'class'):
                GI += 1
                if(TKs[GI].CP == 'ID'):
                    CN=TKs[GI].VP
                    GI += 1
                    Par=Inheri(TKs)
                    if(Par==False):
                        return False
                    if(Par or Par==''):
                        if(Par):
                            CLSTBL.InsertCT(CN,Par)
                        else:
                            CLSTBL.InsertCT(CN,'')
                        if(ClassBody(TKs,CN)):
                            return True
    else:
        return False


def ToDec(TKs):
    global GI
    ToDec_sel = ['tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in ToDec_sel):
        GI += 1
        print(GI)
        return TKs[GI-1].VP
    return False


def xOpts(TKs):
    global GI
    xOpts_sel=['int','AOP']
    if(TKs[GI].CP in xOpts_sel):
        if(TKs[GI].CP=='int'):
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
    if(TKs[GI].CP=='int'):
        GI+=1
        if(TKs[GI].CP==':'):
            GI+=1
            if(TKs[GI].CP=='int'):
                return True
    else:
        return False

def FactorBrackets(TKs):
    global GI
    FactorBrackets_sel=['int',']']
    if(TKs[GI].CP in FactorBrackets_sel):
        if(xOpts(TKs)):
            return True
        elif(Slice(TKs)):
            return True
    else:
        return False

def xOpts2(TKs,CN,AM,T,TM,S):
    global GI
    xOpts2_sel=['ID','[','.','AOP']
    if(TKs[GI].CP in xOpts2_sel):
        T=FactorID(TKs,CN,AM,TM,'',S)
        if(T):
            return T
        elif(x(TKs,CN,AM,T,TM,S)):
            return True
    else:
        return False

def x(TKs,CN,AM,T,TM,S):
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
            OP=TKs[GI].CP
            GI+=1
            T2=xOpts2(TKs,T,AM,T,TM,S)
            T=Compatibility(T,T2,OP)
            if(T==None):
                print('TypeMismatch on line ', TKs[GI].LineNo)
            if(T):
                return T     
        return T
    else:
        return False

def StuffDic(TKs):
    global GI
    StuffDic_sel=['ID', 'int','float', 'char', 'string','(', 'not', 'True', 'False',':']
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
    Dic_sel=['ID', 'int','float', 'char', 'string','(', 'not', 'True', 'False',':']
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
    if(TKs[GI].CP=='('):
        GI+=1
        if(OEL(TKs)):
            if(TK[GI].CP==')'):
                return True
    else:
        return False

def InitOpts(TKs,CN,AM,T,TM,S):
    global GI
    InitOpts_sel=['ID', 'int','float', 'char', 'string', '(','{','[','this', 'not', 'True', 'False']
    if(TKs[GI].CP in InitOpts_sel):
        # T=FactorID(TKs,CN,AM,TM,T,S)
        T=OE(TKs,CN,AM,'',TM,S)
        if(T):
            return T
        # elif (OE(TKs)):
        #     return True
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
        elif(Init(TKs,CN,AM,T,TM,S)):
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

def Init(TKs,CN,AM,T,TM,S):
    global GI
    Init_sel=['ID', 'int',
             'float', 'char', 'string', '(', 'not', 'True', 'False','AOP',',']
    if(TKs[GI].CP in Init_sel):
        if(TKs[GI].CP=='AOP'):
            OP=TKs[GI].VP
            GI+=1
            T2=InitOpts(TKs,CN,AM,T,TM,S)
            with open('IC.txt','a') as f:
                f.write(T+'='+T2+OP+T)
                f.write('\n')
            # T=Compatibility(T,T2,OP)
            if(T==None or T==''):
                print('TypeMismatch on line ', TKs[GI].LineNo)
            if(T):
                return T
        return True
    else:
        return False



def FI2Opts(TKs,CN,AM,T,TM,S):
    global GI
    FI2Opts_sel=['ID', 'int',
             'float', 'char', 'string', '(', 'not', 'True', 'False','static','DT','tuple','dict','var','this',',']
    if(TKs[GI].CP in FI2Opts_sel):
        if(OEL2(TKs,CN,AM,T,TM,S)):
            return True
    else:
        return False

def FactorID2(TKs,CN,AM,T,TM,S):
    global GI
    FactorID2_sel = ['[', '.','AOP',',']
    if(TKs[GI].CP in FactorID2_sel):
        if(x(TKs,CN,AM,T,TM,S)):
            if(Init(TKs,CN,AM,T,TM,S)):
                if(FI2Opts(TKs,CN,AM,T,TM,S)):
                    return True
    else:
        return False

# def FCOptsL(TKs):
#     global GI
#     FCOptsL_sel=['AOP','ID','int','float','char','string','not','(','True','False']
#     if(TKs[GI].CP in FCOptsL_sel):
#         if(Init(TKs)):
#             if(OEL(TKs)):
#                 return True
#         elif(OE(TKs)):
#             if(OEL2(TKs)):
#                 return True

def FCOpts(TKs,CN,AM,T,TM,S):
    global GI
    FCOptsL_sel=['static','DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in FCOptsL_sel):
        if(OEL(TKs,CN,AM,T,TM,S)):
            return True
    return False

def FactorComma(TKs,CN,AM,T,TM,S):
    global GI
    if(TKs[GI].CP==','):
        if(TKs[GI].CP==','):
            GI+=1
            if(FCOpts(TKs,CN,AM,T,TM,S)):
                return True
        return True
    else:
        return False

def OEL2(TKs,CN,AM,T,TM,S):
    global GI
    if(TKs[GI].CP==','):
        if(FactorComma(TKs,CN,AM,T,TM,S)):
            return True
        return True
    else:
        return False

def OEL(TKs,CN,AM,T,TM,S):
    global GI
    OEL_sel=['ID', 'int',
             'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in OEL_sel):
        T=OE(TKs,CN,AM,T,TM,S,0)
        if(T):
            if(OEL2(TKs,CN,AM,T,TM,S)):
                return True
        return True
    else:
        return False

def FactorBraces(TKs,CN,AM,T,TM,S,*args):
    global GI
    tem=None
    if(len(args)>0):
        tem=args[0]
    FactorBraces_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
                        'float', 'char', 'string', '(', 'not', 'True', 'False', ',', ')']
    if(TKs[GI].CP in FactorBraces_sel):
        # if(OEL(TKs,CN,AM,'',TM,S)):
        #     return True
        T=PL(TKs,'',CN,AM,S,None)
        if (T):
            return T
        return True
    else:
        return False

def FnCall(TKs,CN,AM,T,TM,S):
    global GI
    if(TKs[GI].CP=='ID'):
        if(FactorID(TKs,CN,AM,T,TM,S)):
            return True
    else:
        return False    



def T(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    T_sel = ['ID', 'int',
             'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in T_sel):
        Tv=FactorID(TKs,CN,AM,TM,Tv,S)
        if(Tv):
            Tv2=OE(TKs,CN,AM,Tv,TM,S,0)
            if(Tv2):
                return Tv2
            return Tv
        if(TKs[GI].CP=='int' or TKs[GI].CP=='float' or TKs[GI].CP=='char' or TKs[GI].CP=='string'):
            Tv=TKs[GI].VP
            GI+=1
            return Tv
        Tv=FnCall(TKs,CN,AM,T,TM,S)
        if(Tv):
            return Tv
        if(TKs[GI].CP=='('):
            GI+=1
            Tv=FnCall(TKs,CN,AM,T,TM,S)
            if(T):
                if(TKs[GI].CP==')'):
                    GI+=1
                    return Tv
        if(TKs[GI].CP=='not'):
            GI+=1
            Tv=T(TKs,Tv,CN,AM,TM,S)
            if(Tv):
                with open('IC.txt','a') as f:
                    f.write('not'+Tv)
                    f.write('\n')
                return Tv
        # elif(IncDec(TKs,'','','','',S)):
        #     return op
        if(TKs[GI].CP=='True'):
            return 'bool'
        if(TKs[GI].CP=='False'):
            return 'bool'

def NT_(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    # T=CreatTemp()
    NT__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False', ',', ')', ':', 'or', 'and', 'ROP', 'PM','MDM',';']
    if(TKs[GI].CP in NT__sel):
        # T=CreatTemp()
        if(TKs[GI].CP == 'MDM'):
            Tt=CreatTemp()
            op=TKs[GI].VP
            GI += 1
            T1=T(TKs,'',CN,AM,TM,S)
            # Tv=Compatibility(Tv,T1,op)
            Tv=NT_(TKs,Tv,CN,AM,TM,S)
            with open('IC.txt','a') as f:
                f.write(Tt+'='+Tv+op+T1)
                f.write('\n')
            if(Tv):
                return Tv
        return Tv
    else:
        return ''

def NT(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    NT_sel = ['ID', 'int',
             'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in NT_sel):
        Tv=T(TKs,Tv,CN,AM,TM,S,args[0])
        if(Tv):
            Tv2=NT_(TKs,Tv,CN,AM,TM,S,args[0])
            if(Tv2):
                return Tv2
            return Tv
    else:
        return ''

def E_(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    # T=CreatTemp()
    E__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False', ',', ')', ':', 'or', 'and', 'ROP', 'PM',';']
    if(TKs[GI].CP in E__sel):
        # T=CreatTemp()
        if(TKs[GI].CP == 'PM'):
            T=CreatTemp()
            op=TKs[GI].VP
            GI += 1
            T1=NT(TKs,'',CN,AM,TM,S,args[0])
            # Tv=Compatibility(Tv,T1,op)
            Tv=E_(TKs,Tv,CN,AM,TM,S,args[0])
            with open('IC.txt','a') as f:
                f.write(T+'='+Tv+op+T1)
                f.write('\n')
            if(Tv):
                return Tv
        return Tv
    else:
        return ''


def E(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    E_sel = ['ID', 'int',
             'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in E_sel):
        Tv=NT(TKs,Tv,CN,AM,TM,S,args[0])
        if(Tv):
            Tv2=E_(TKs,Tv,CN,AM,TM,S,args[0])
            if(Tv2):
                return Tv2
            return Tv
    else:
        return ''


def RE_(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    # T=CreatTemp()
    RE__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
               'float', 'char', 'string', '(', 'not', 'True', 'False', ',', ')', ':', 'or', 'and', 'ROP',';']
    if(TKs[GI].CP in RE__sel):
        # T=CreatTemp()
        if(TKs[GI].CP == 'ROP'):
            T=CreatTemp()
            op=TKs[GI].VP
            GI += 1
            T1=E(TKs,'',CN,AM,TM,S,args[0])
            # Tv=Compatibility(Tv,T1,op)
            Tv=RE_(TKs,Tv,CN,AM,TM,S,args[0])
            with open('IC.txt','a') as f:
                f.write(T+'='+Tv+op+T1)
                f.write('\n')
            if(Tv):
                return Tv
        return Tv
    else:
        return ''


def RE(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    RE_sel = ['ID', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in RE_sel):
        Tv=E(TKs,Tv,CN,AM,TM,S,args[0])
        if(Tv):
            Tv2=RE_(TKs,Tv,CN,AM,TM,S,args[0])
            if(Tv2):
                return Tv2
            return Tv
    else:
        return ''


def AE_(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    # T=CreatTemp()
    AE__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
               'float', 'char', 'string', '(', 'not', 'True', 'False', ',', ')', ':', 'or', 'and',';']
    if(TKs[GI].CP in AE__sel):
        # T=CreatTemp()
        if(TKs[GI].CP == 'and'):
            T=CreatTemp()
            op=TKs[GI].VP
            GI += 1
            T1=RE(TKs,'',CN,AM,TM,S,args[0])
            # Tv=Compatibility(Tv,T1,op)
            with open('IC.txt','a') as f:
                f.write(T+'='+Tv+op+T1)
                f.write('\n')
            Tv=AE_(TKs,Tv,CN,AM,TM,S,args[0])
            if(Tv):
                return Tv
        return Tv
    else:
        return ''


def AE(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    AE_sel = ['ID', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in AE_sel):
        Tv=RE(TKs,Tv,CN,AM,TM,S,args[0])
        if(Tv):
            Tv2=AE_(TKs,Tv,CN,AM,TM,S,args[0])
            if(Tv2):
                return Tv2
            return Tv
    else:
        return ''


def OE_(TKs,Tv,CN,AM,TM,S,*args):
    global GI
    OE__sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var', 'this', 'int',
               'float', 'char', 'string', '(', 'not', 'True', 'False', ',', ')', ':', 'or',';']
    if(TKs[GI].CP in OE__sel):
        if(TKs[GI].CP == 'or'):
            T=CreatTemp()
            op=TKs[GI].VP
            GI += 1
            T1=AE(TKs,'',CN,AM,TM,S,args[0])
            # Tv=Compatibility(Tv,T1,op)
            with open('IC.txt','a') as f:
                f.write(T+'='+Tv+op+T1)
                f.write('\n')
            Tv=OE_(TKs,Tv,CN,AM,TM,S,args[0])
            if(Tv):
                return Tv
        return Tv
    else:
        return ''


def OE(TKs,CN,AM,T,TM,S,*args):
    global GI
    tem=None
    OE_sel = ['ID', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False']
    if(TKs[GI].CP in OE_sel):
        if(len(args)>0):
            tem=args[0]
        Tv=AE(TKs,T,CN,AM,TM,S,tem)
        if(Tv):
            Tv2=OE_(TKs,Tv,CN,AM,TM,S,tem)
            if(Tv2):
                return Tv2
            return Tv
    else:
        return ''


def IncDecOp(TKs):
    global GI
    if(TKs[GI].CP == 'AOP'):
        op=TKs[GI].VP
        GI += 1
        return op


def FIOpts(TKs,CN,AM,T,TM,S,*args):
    global GI
    print(GI)
    T2=T
    FIOpts_sel = ['AOP', '(', '[', '.',',','ID', 'int',
              'float', 'char', 'string', '(', 'not', 'True', 'False',';',')','ROP']
    if(TKs[GI].CP in FIOpts_sel):
        # GI += 1
        Op=IncDecOp(TKs)
        if(Op):
            
            T1=OE(TKs,CN,AM,'',TM,S,0)
            print(GI)
            if(T1 and TKs[GI].VP!='.'):
                # T=Compatibility(T2,T1,Op)
                if(T==None):
                    print('Type Mismatch Error at line ',TKs[GI].LineNo)
                    return False
                return True
            T3=x(TKs,CN,AM,T1,TM,S)
            Tt=T3
            if(T3):
                Tt=x(TKs,CN,AM,T3,TM,S)
                if(Tt):
                    T=Compatibility(T2,Tt,Op)
                else:
                    T=Compatibility(T2,T3,Op)
            if(T==None):
                print('Type Mismatch Error at line ',TKs[GI].LineNo)
                return False
            return True
        if(TKs[GI].CP=='ROP'):
            op=TKs[GI].VP
            T1=OE(TKs,S)
            if(T1):
                T=Compatibility(T,T1,Op)
                if(T==None):
                    print('Type Mismatch Error at line ',TKs[GI].LineNo)
                    return False
                return True
        elif(TKs[GI].CP == '('):
            S=CreateScope()
            GI += 1
            N=args[0]
            T=FactorBraces(TKs,CN,AM,T,TM,S,1)
            if(T):
                if(TKs[GI].CP == ')'):
                    S=DestroyScope()
                    GI += 1
                    return True
        elif FactorID2(TKs,CN,AM,T,TM,S):
            return True
        elif(OE(TKs,CN,AM,T,TM,S,0)):
            return True
        return True
    else:
        return False

def FactorID(TKs,CN,AM,TM,T,S,*args):
    global GI
    flag=0
    flag2=0
    if(TKs[GI].CP == 'ID'):
        N=TKs[GI].VP
        GI += 1
        print(GI)
        if(T==''):
            if(AM or TKs[GI-2].VP=='.'):
                T=CLSTBL.LookupCDT(CN,N,AM,TM)
                return N
            else:
                T=SYMTBL.FnLookupST(N,S)
                if(T==None):
                    T=SYMTBL.LookupST(N,S,T)
                else:
                    return N
                if(T or TKs[GI].VP=='.'):
                    flag2=1
                flag=1
                if(T==None):
                    T=CLSTBL.LookupCT(N)
                    # flag2=1
                    if(T==None):
                        T=SYMTBL.FnLookupST(N,S)
                        flag2=2
                        if(T==None):
                            print("Undeclared Variable Reference ",TKs[GI].VP)
                            return False
                if(flag2!=0 and TKs[GI].VP in WordSplitter.operators):
                    return N
        if((not regex.isKw(T)) and (TKs[GI].VP=='.')):
            if(flag2==0 and TKs[GI].VP=='('):
                pass
            else:
                return N
        if(AM and TKs[GI].CP!='('):
            if(CLSTBL.InsertCDT(CN,N,T,AM,TM)==False and flag!=1):
                print("Redenclaration Error for "+N+" on line Number ", TKs[GI-1].LineNo)
                return False
        elif((AM=='' or AM==None or AM==False)and (TKs[GI].CP!='(') and flag!=1):
            if(SYMTBL.InsertST(N,T,S)==False): 
                print("Redenclaration Error for "+N+" on line Number ", TKs[GI-1].LineNo)
                # GI+=1
                return False
        
        if(FIOpts(TKs,CN,AM,T,TM,S,N)):
            if(len(args)>0):
                if(args[0]==1):
                    return N
            return N
    return False


def Dec(TKs,CN,AM,S):
    global GI
    Dec_sel = ['static', 'tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in Dec_sel):
        TM=StaticOp(TKs)
        if(TM!=False):
            T=ToDec(TKs)
            if(not regex.isKw(T)):
                T=CLSTBL.LookupCT(T)
            if(T!=None):
                N=FactorID(TKs,CN,AM,TM,T,S)
                if(N!=False):
                    return T
    return False


def NewDec(TKs,CN,AM,S):
    global GI
    NewDec_sel = ['static', 'tuple', 'DT', 'dict', 'ID', 'var']
    if(TKs[GI].CP in NewDec_sel):
        if(Dec(TKs,CN,AM,S)):
            if(TKs[GI].CP == ';'):
                GI += 1
                return True
    else:
        return False


def GlobalDefs(TKs,S):
    global GI
    CN=''
    AM=''
    GlobalDefs_sel = ['static', 'DT', 'tuple', 'dict', 'ID', 'var']
    print(TKs[GI].CP)
    if(TKs[GI].CP in GlobalDefs_sel):
        if(NewDec(TKs,CN,AM,S)):
            if(GlobalDefs(TKs,S)):
                return True
            return True
    else:
        return False

def BodyOpts(TKs,CN,AM,TM,S):
    global GI
    BodyOpts_sel=[';','{','ID','this','while','if','for','return','def',
                'AM','static','abstract','class','DT','tuple','dict','ID','var','main','$']
    if(TKs[GI].CP in BodyOpts_sel):
        if(Body(TKs,CN,AM,TM,S)):
            return True
        return True
    else:
        return False

def FnDec2(TKs,CN,AM,TM,S):
    global GI
    if(TKs[GI].CP=='def'):
        if(FnDec(TKs,CN,AM,TM,S)):
            if(BodyOpts(TKs,CN,AM,TM,S)):
                return True
    else:
        return False

def Defs(TKs,S):
    global GI
    
    Defs_sel = ['def', 'AM', 'static', 'abstract', 'class',
                'DT', 'tuple', 'dict', 'ID', 'var', 'main', '$']
    if(TKs[GI].CP in Defs_sel):
        print(GI)
        if(FnDec2(TKs,'','','',S)):
            if(Defs(TKs,S)):
                return True
            return True
        elif(ClassDec(TKs,S)):
            if(Defs(TKs,S)):
                return True
            return True
        elif(GlobalDefs(TKs,S)):
            if(Defs(TKs,S)):
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
    
    S=CreateScope()
    Start_sel = ['def', 'public', 'private', 'protected', 'sealed', 'static',
                 'abstract', 'class', 'DT', 'tuple', 'dict', 'ID', 'var','main']
    if(TKs[GI].CP in Start_sel):
        print(GI)
        if(Defs(TKs,S)):
            if(TKs[GI].CP == 'main'):
                GI += 1
                if(TKs[GI].CP == '('):
                    GI += 1
                    if(TKs[GI].CP == ')'):
                        GI += 1
                        if(TKs[GI].CP == '{'):
                            GI += 1
                            AM=''
                            TM=''
                            CN=''
                            S=CreateScope()
                            if(MST(TKs,CN,AM,TM,S)):
                                if(TKs[GI].CP == '}'):
                                    S=DestroyScope()
                                    GI += 1
                                    if(Defs(TKs,S)):
                                        return True
        # return True
    else:
        return False


def SA(TKs):
    global GI
    Start(TKs)
    # if(Start(TKs)):
    #     print("Valid Syntax and Semantics")
    # else:
    #     print("Error at Line Number ", TKs[GI].LineNo)