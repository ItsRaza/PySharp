
ST = []


class SymbolTable:
    Name = ""
    Type = ""
    Scope = None

    # def __init__(self):

    def InsertST(self, N, T, S):
        check = self.LookupST(N, S)
        if(check):
            return False
        temp = SymbolTable()
        temp.Name = N
        temp.Type = T
        temp.Scope = S
        ST.append(temp)
        return True

    def LookupST(self, N, S):
        for s in ST:
            if(N == s.Name and S == s.Scope):
                print(N+" found")
                return s.Type

    def PrintST(self):
        for s in ST:
            print(s.Name + ',' + s.Type + ',' + s.Scope)
