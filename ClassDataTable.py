

class ClassDataTable:
    Name = ""
    Type = ""
    AM = ""
    TM = ""
    CDT = []

    def __init__(self):
        self.Name = None
        self.Type = None
        self.AM = None
        self.TM = None
        self.CDT = []

    def InsertCDT2(self, N, T, AM, TM):
        check = self.LookupCDT2(N, AM, TM)
        if(check):
            return False
        temp = ClassDataTable()
        temp.Name = N
        temp.Type = T
        temp.AM = AM
        temp.TM = TM
        self.CDT.append(temp)
        print(temp.Name, ' Inserted in ClassData Table')
        return True

    def LookupCDT2(self, N, AM, TM):
        if(self.CDT != None):
            for s in self.CDT:
                if(N == s.Name):
                    print(N+" found")
                    return s.Type

    def PrintCDT(self):
        for s in self.CDT:
            print(s.Name + ',' + s.Type + ',' + s.TM + ',' + s.AM)

    def FnLookupST(self, N):
        for s in ST:
            T = ''
            if(N == s.Type or N == s.Name):
                print(N+" found")
                return s.Type
