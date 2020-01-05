import regex
import WordSplitter
import LA
import SA
import Semantic
import SymbolTable
import ClassDataTable
import ClassTable

# st = SymbolTable.SymbolTable()

# st.InsertST('a', 'int', 0)
# st.InsertST('a', 'int', 0)
# st.InsertST('c', 'int', 0)
# # st.PrintST()
# # T = st.LookupST('c', 0)
# # print(T)

# cdt2 = ClassDataTable.ClassDataTable()
# cdt = ClassDataTable.ClassDataTable()
# cdt.InsertCDT('a', 'int', 'public', '')
# cdt.InsertCDT('b', 'int', 'private', 'virtual')
# cdt.InsertCDT('fn', 'int,int->void', 'public', '')
# # cdt.PrintCDT()
# # print('\n')
# # cdt2.PrintCDT()

# ct = ClassTable.ClassTable()
# ct.InsertCT('foo', 'bar')
# ct.InsertCDT('foo', 'fn', 'int,int->void', 'public', '')
# ct.InsertCDT('foo', 'fn2', 'int->int', 'public', '')
# ct.InsertCT('foo2', 'bar2')
# ct.InsertCDT('foo2', 'f', 'void->void', 'private', 'override')
# ct.PrintCT()

# ct.LookupCDT('foo', 'fn2', 'int->int', 'public', '')


TKs = LA.lexer('SETest1.txt')
print(len(TKs))
for T in TKs:
    print(T.CP)

print('\n')


Semantic.SA(TKs)
