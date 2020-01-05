
ST = []


class SymbolTable:
    Name = ""
    Type = ""
    Scope = None

    # def __init__(self):

    def InsertST(self, N, T, S):
        check = self.LookupST(N, S, T)
        if(check == False):
            return False
        temp = SymbolTable()
        temp.Name = N
        temp.Type = T
        temp.Scope = S
        ST.append(temp)
        print(temp.Name, ' Inserted in Symbol Table in scope ', temp.Scope)
        return True

    def LookupST(self, N, S, T):
        for s in ST:
            if(N == s.Name):
                print(N+" found")
                if(S == s.Scope and T != ''):
                    return False
                return s.Type

    def FnLookupST(self, N, S):
        for s in ST:
            T = ''
            if(N == s.Name):
                print(N+" found")
                return s.Type

    def PrintST(self):
        for s in ST:
            print(s.Name + ',' + s.Type + ',' + s.Scope)
