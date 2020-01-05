import ClassDataTable

CT = []


def Return(N):
    for s in CT:
        if(N == s.Name):
            return s


class ClassTable:
    Name = ""
    Type = "class"
    Parent = ""
    ref = ClassDataTable.ClassDataTable()

    def InsertCT(self, N, Par):
        check = self.LookupCT(N)
        if(check):
            return False
        temp = ClassTable()
        temp.Name = N
        temp.Parent = Par
        temp.ref = ClassDataTable.ClassDataTable()
        CT.append(temp)
        print(temp.Name, ' Inserted in Class Table')
        return True

    def LookupCT(self, N):
        for s in CT:
            if(N == s.Name):
                print(N+" found")
                return s.Name

    def PrintCT(self):
        for s in CT:
            print(s.Name + ',' + s.Type + ',' + s.Parent)
            s.ref.PrintCDT()

    def InsertCDT(self, CN, N, T, AM, TM):
        req = Return(CN)
        req.ref.InsertCDT2(N, T, AM, TM)

    def LookupCDT(self, CN, N, AM, TM):
        req = Return(CN)
        T = req.ref.LookupCDT2(N, AM, TM)
        return T
