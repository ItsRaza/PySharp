import regex
import WordSplitter
import LA
import SA
import Semantic
import SymbolTable
import ClassDataTable
import ClassTable
import ICG

TKs = LA.lexer('SETest1.txt')
print(len(TKs))
for T in TKs:
    print(T.CP)

print('\n')

# print(ICG.CreateLable())

Semantic.SA(TKs)
# ICG.SA(TKs)
