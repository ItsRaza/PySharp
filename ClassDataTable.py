

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
        check = self.LookupCDT2(N, T, AM, TM)
        if(check):
            return False
        temp = ClassDataTable()
        temp.Name = N
        temp.Type = T
        temp.AM = AM
        temp.TM = TM
        self.CDT.append(temp)
        return True

    def LookupCDT2(self, N, T, AM, TM):
        if(self.CDT != None):
            for s in self.CDT:
                if(N == s.Name and T == s.Type and AM == s.AM and TM == s.TM):
                    print(N+" found")
                    return s.Type

    def PrintCDT(self):
        for s in self.CDT:
            print(s.Name + ',' + s.Type + ',' + s.TM + ',' + s.AM)
