'''
CS308 Section W01
Concepts of programming Languages
Stanley Gilstrap
Parser/Lexical Analyzer
Deliverable 2
'''
class Parser:
    #global variables
    reserved_words = ['function', 'if', 'end', 'then', 'else', 'while', 'do', 'repeat', 'until', 'print']
    operationType = ''
    arithmeticCounter = 0

    isComparator = False
    isEquals = False
    comparatorStarted = False
    isArithmetic = False
    functionStarted = False
    assignStarted = False
    boolStarted = False
    ifStarted = False
    thenStarted = False
    elseStarted = False
    whileStarted = False
    printStarted = False
    doStarted = False
    repeatStarted = False
    untilStarted = False
    nextToken = ''
    nextLex = ''

    def printLex(self,lex,tokenType):#Prints out token type and lexeme coming from scanner
        print(lex,tokenType)

    def function(self): #Starts function non-terminal
        print('start function')
        Parser.functionStarted = True

    def end(self): #ends function, if, then, else, while, do, and print statements
        #print('end')
        if(Parser.ifStarted == False
           and Parser.whileStarted == False
           and Parser.thenStarted == False
           and Parser.elseStarted == False):
                Parser.functionStarted = False
                print('function ended')
        if Parser.ifStarted:
            Parser.ifStarted = False
            print('if ended')
        if Parser.thenStarted:
            Parser.thenStarted = False
            print('then ended')
        if Parser.elseStarted:
            Parser.elseStarted = False
            print('else ended')
        if Parser.whileStarted:
            Parser.whileStarted = False
            print('while ended')
        if Parser.doStarted:
            Parser.doStarted = False
            print('do ended')

    def if_statement(self):
        Parser.ifStarted = True
        print('start if statement')
        Parser.operationType = 'if'
    def then_statement(self):
        Parser.thenStarted = True
        Parser.comparatorStarted = False
        print('then started')
        Parser.operationType = 'then'
    def else_statement(self):
        Parser.elseStarted = True
        print('else started')
        Parser.operationType = 'else'
    def while_statement(self):
        Parser.whileStarted = True
        print('while started')
        Parser.operationType = 'while'
    def do_statement(self):
        Parser.doStarted = True
        print('do started')
        Parser.operationType = 'do'
    def assignment_statement(self):
        Parser.assignStarted = True
        print('assignment started')
        print(Parser.nextLex)
        Parser.operationType = 'assignment'
    def repeat_statement(self):
        Parser.repeatStarted = True
        print('repeat started')
        Parser.operationType = 'repeat'
    def until_statement(self):
        Parser.repeatStarted = False
        print('repeat ends')
        Parser.untilStarted = True
        print('until started')
        Parser.operationType = 'until'
    def print_statement(self):
        Parser.printStarted = True
        print('print started')
        Parser.operationType = 'print'
    def bool_expression(self):
        print('boolean started')
        Parser.boolStarted = True
        Parser.operationType = 'boolean'
    def arithmetic_statement(self):
        Parser.isArithmetic = True
        print('arithmetic started')

    def select(self,lex,tokenType): #Reads incoming token/lexeme and selects what is to be done with them
        #print(lex, tokenType)
        Parser.nextLex = lex
        Parser.nextToken = tokenType
        if(tokenType == 'id'):
            if lex in Parser.reserved_words:
                if lex == 'function':
                    if not Parser.functionStarted:
                        Parser.function(self)
                    else:
                        print('ERROR: Function already in progress')
                elif lex == 'end':
                    Parser.end(self)
                elif lex == 'if':
                    Parser.if_statement(self)
                elif lex == 'then':
                    if Parser.ifStarted:
                        Parser.then_statement(self)
                    else:
                        print('ERROR: then without matching if')
                elif lex == 'else':
                    if Parser.ifStarted and Parser.thenStarted:
                        Parser.else_statement(self)
                    else:
                        print('ERROR: else without matching if')
                elif lex == 'while':
                    Parser.while_statement(self)
                elif lex =='do':
                    Parser.do_statement(self)
                elif lex == 'repeat':
                    Parser.repeat_statement(self)
                elif lex == 'until':
                    if Parser.repeatStarted:
                        Parser.until_statement(self)
                    else:
                        print('ERROR: until without matching repeat')
                elif lex == 'print':
                    Parser.print_statement(self)
            else:# TODO These are ids used in booleans and arithmetic and comparators
                #print('ids',Parser.boolStarted, Parser.isArithmetic)
                if Parser.boolStarted == False and Parser.isArithmetic == False and Parser.comparatorStarted == False:
                    #print('assign id')
                    Parser.assignment_statement(self)
                elif Parser.isArithmetic:
                       # print(Parser.arithmeticCounter)
                        if Parser.arithmeticCounter <= 1:
                            print(lex)  # prints id in an arithmetic statement
                            Parser.arithmeticCounter = Parser.arithmeticCounter + 1
                            if Parser.arithmeticCounter >= 2:
                                Parser.isArithmetic = False
                                Parser.arithmeticCounter = 0

                                print('arithmetic ended')
                                if Parser.assignStarted:
                                        Parser.assignStarted = False
                                        print('assignment ended')
                elif Parser.comparatorStarted:
                    if Parser.arithmeticCounter <= 1:
                        print(lex)  # prints id in an arithmetic statement
                        Parser.arithmeticCounter = Parser.arithmeticCounter + 1
                        if Parser.arithmeticCounter >= 2:
                            Parser.comparatorStarted = False
                            Parser.arithmeticCounter = 0
                            print(Parser.operationType,'ended')
                            if Parser.ifStarted:
                                Parser.ifStarted = False
                                print('if ended')
                elif Parser.boolStarted:
                    print(lex)
        elif tokenType == 'literal_integer':
            if not Parser.isArithmetic:
                print(lex)
                print(Parser.operationType, 'ended')
                Parser.arithmeticCounter = 0
            else:
                if Parser.arithmeticCounter <= 1:
                    print(lex)  # prints id in an arithmetic statement
                    Parser.arithmeticCounter = Parser.arithmeticCounter + 1
                    if Parser.arithmeticCounter >= 2:
                        Parser.isArithmetic = False
                        Parser.arithmeticCounter = 0
                        print(Parser.operationType, 'ended')
                        if Parser.assignStarted:
                            Parser.assignStarted = False
                            print('assignment ended')
                        elif Parser.comparatorStarted:
                            Parser.comparatorStarted = False


        elif tokenType == 'eq_operator':
            Parser.comparatorStarted = True
            Parser.operationType = 'eq comparator'
            print('eq comparator start')
            print(lex)

        elif tokenType == 'assignment_operator':
            if Parser.assignStarted:
                print('=')
        elif tokenType == 'lt_operator':
            Parser.comparatorStarted = True
            Parser.operationType = 'lt comparator'
            print('lt comparator start')
            print(lex)
        elif tokenType == 'le_operator':
           Parser.comparatorStarted = True
           Parser.operationType = 'le comparator'
           print('le comparator start')
           print(lex)

        elif tokenType == 'ge_operator':
            Parser.comparatorStarted = True
            Parser.operationType = 'ge comparator'
            print('ge comparator start')
            print(lex)

        elif tokenType == 'ne_operator':
            Parser.comparatorStarted = True
            Parser.operationType = 'ne comparator'
            print('ne comparator start')
            print(lex)

        elif tokenType == 'add_operator':
            Parser.arithmetic_statement(self)
            Parser.operationType = 'add operator'
            print('add operation start')
            print('+')
        elif tokenType == 'sub_operator':
            Parser.arithmetic_statement(self)
            Parser.operationType = 'sub operator'
            print('sub operation start')
            print('-')
        elif tokenType == 'mul_operator':
            Parser.arithmetic_statement(self)
            Parser.operationType = 'mul operator'
            print('mul operation start')
            print('*')
        elif tokenType == 'div_operator':
            Parser.arithmetic_statement(self)
            Parser.operationType = 'div operator'
            print('div operation start')
            print('/')
        elif tokenType == 'left_parenthesis':
            pass
        elif tokenType == 'right_parenthesis':
            print('print ended')



