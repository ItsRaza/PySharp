import regex
import WordSplitter
import LA

txt = "void main()\n{\nint a= -558;\nInt a++=='ajfjds as \" ae=9987'\nchar b='a;\n}"

# stri = LA.readFile("data.txt")
words = WordSplitter.BreakWord(txt)
print(words)

TKs = LA.lexer('code.txt')
print(len(TKs))
for T in TKs:
    print(T.CP)

i = 0
with open("tokens.txt", "a") as myfile:
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
