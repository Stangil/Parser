'''
CS308 Section W01
Concepts of programming Languages
Stanley Gilstrap
Parser/Lexical Analyzer
Deliverable 2
'''
from Parser import Parser
class LexicalAnalyzer:
    __nextChar = ''
    __charClass = 0
    __lexLen = 0
    __nextToken = ""
    __line = ""
    __lexeme = []
    __isComparator = False
    __tokenLibrary = {'==': "eq_operator", '=': "assignment_operator", '<': "lt_operator", '>': 'gt_operator',
                    '<=': "le_operator", '>=': "ge_operator", '~=': "ne_operator", '+': "add_operator",
                      '-': "sub_operator", '*': "mul_operator", '/': "div_operator", '(': "left_parenthesis",
                      ')': "right_parenthesis"}

    def __init__(self, fileName):#Takes file name as a parameter
        if fileName is None:
            raise ValueError("invalid fileName argument")
        self.fileName = fileName
        newFile = open(fileName)
        self.__line = newFile.readline()#reads first line into a list
        while self.__line:#Looping through each line of test file
            self.processLine(self.__line)
            self.__line = newFile.readline()

    def processLine(self, l): #separate each character in line
        for i in l:
            self.__nextChar = i
            self.getCharClass(i)
            self.lex(i)
        self.__lexeme = []

    def getCharClass(self, char): # sets char class to proper int for incoming character

        if char.isalpha():
            self.__charClass = 1
        elif char.isnumeric():
            self.__charClass = 2
        elif char.isspace():
            self.__charClass = 4
        elif char == '\n':
            self.__charClass = 5
        else:
            self.__charClass = 3 #if character is a paran or operator or other

    def lex(self, i):
        if i.isspace():

            self.nextLexeme()
        else:
            if len(self.__lexeme) == 0:#When lexeme is empty
                self.addChar(i)#add character if lexeme is empty
                if self.__charClass == 1:
                    self.__nextToken = 'id'
                elif self.__charClass == 2:
                    self.__nextToken = 'literal_integer'
                elif self.__charClass == 3:
                    if (i == '(' or i == ')' or i == '+' or i == '-' or i == '/' or i == '*'):
                        self.lookUpSingleSymbol(i)
                    elif (i == '<' or i == '>' or i == '=' or i == '~'):
                        self.lookUpCompareSymbol(i)
                    else:
                        print("ERROR SYMBOL",i, "NOT FOUND")
                        self.__lexeme = []

            #When lexeme is not empty
            else:
                if self.__lexeme[0].isalpha and self.__charClass == 1:#checking for letter
                    self.addChar(i)
                elif self.__lexeme[0].isdigit and self.__charClass == 2:
                    self.addChar(i)
                elif self.__isComparator == False and self.__charClass == 3:
                    self.nextLexeme()
                    self.addChar(i)
                    self.lookUpSingleSymbol(i)
                elif self.__isComparator == True and self.__charClass == 3:
                    if len(self.__lexeme) < 2:
                        self.addChar(i)
                        self.lookUpCompareSymbol(i)
                    else:
                        print("ERROR: Comparators only use 1 or 2 characters")

    def addChar(self, char):
        if len(self.__lexeme) <= 98:
                self.__lexeme.append(char)
        else:
            print("ERROR: lexeme is too long")

    def lookUpSingleSymbol(self, i): #lookup symbols in tokenlibrary, set the proper token, add to lexeme, and reset lexeme
        self.__nextToken = self.__tokenLibrary[i]
        self.nextLexeme()

    def lookUpCompareSymbol(self, i):#lookup symbols in tokenlibrary, set the proper token, add to lexeme, and reset lexeme
        self.__isComparator = True
        lex1 = str(''.join(self.__lexeme))
        if(lex1 in self.__tokenLibrary):
            self.__nextToken = self.__tokenLibrary[lex1]

    def nextLexeme(self): #Sends lexeme and token to parser
        if(len(self.__lexeme)> 0):
            Parser.select(self,str(''.join(self.__lexeme)),self.__nextToken)
            self.__lexeme = []
            self.__isComparator = False


