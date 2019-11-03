import regex
import WordSplitter
import LA


txt = 'my name is "15.23\n12.ab6.24'
bla = WordSplitter.BreakWord(txt)
print(bla)

'''
TKs = LA.lexer('code.txt')
print(len(TKs))
for T in TKs:
    print(T.CP)

i = 0
with open("tokens3.txt", "a") as myfile:
    for T in TKs:
        myfile.write("Token "+str(i)+":")
        myfile.write("\n")
        myfile.write("Class: "+T.CP)
        myfile.write("\n")
        myfile.write("Value: "+T.VP)
        myfile.write("\n")
        myfile.write("Line: "+str(T.LineNo))
        myfile.write("\n")
        myfile.write("\n")
        myfile.write("\n")
        i += 1
'''
