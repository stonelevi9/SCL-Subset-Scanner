
import json
# Here we initialize all our variables to be used later on keywords, identifiers, operators, constants, and strings,
# are all arrays that hold data based on their titles varFound is a boolean that denotes we found a keyword that
# denotes a variable name is up next globalVar is a boolean that denotes we are underneath the variables section in
# global declarations globalCon is a boolean that denotes we are underneath the constants section in global
# declarations stringFound is a boolean that denotes we have found a string commentFound is a boolean that denotes we
# have found comments tempString is used to append and store words that belong to a string together back into a
# string phase is an integer that keeps track of what keyword block we are within tempPhase is a pointer that is used
# to point back to whatever keyword block we are within if we find comments we must deal with inside that block.
keywords = []
identifiers = []
operators = []
constants = []
strings = []
varFound = False
globalVar = False
globalCon = False
stringFound = False
commentFound = False
conFound = False
tempString = ""
phase = 0
tempPhase = 0
with open('linkedg.scl') as test:
    # We open our scl file and iterate through each line and then in our nested for loop we iterate through each word in
    # the lines
    for line in test:
        currentList = line.split()
        for word in currentList:
            # Here if we find //, we know that we that everything following it on the line will be comments
            if word == "//":
                commentFound = True
            # Here is a conditional statement that deals with everything following the keyword description
            # It has several cases, such our word == description in the case that our phase != 0 and if it does = 0
            # We use our phase variable to keep track of which keyword we are underneath in our scanner
            # The last conditional statement is our ending condition for description, which is when we find */
            if word == "description" or phase == -3:
                if phase != 0 and word == "description":
                    keywords.append(word)
                    tempPhase = phase
                    phase = -3
                if phase == 0 and word == "description":
                    keywords.append(word)
                    phase = -3
                if word == "*/":
                    if tempPhase != 0:
                        phase = tempPhase
                        tempPhase = 0
                        continue
                    if tempPhase == 0:
                        phase = 0
                        continue
            # Here is a conditional statement that deals with everything following the keyword specifications. It has
            # several cases such as if the word equals struct, define, or definetype (which means we have an
            # identifiers name following that keyword), if we have found a variable (from the previous conditional),
            # if the word contains [ and ] which means it refers to an array, and if the words equals forward which
            # is our ending condition for specifications. We also have an else statement that deals with anything
            # that does not fall in any of those conditional statements.
            if (word == "specifications" or phase == 5) and commentFound is False:
                phase = 5
                if word == "struct" or word == "define" or word == "definetype":
                    varFound = True
                    keywords.append(word)
                elif word == "forward":
                    phase = 0
                elif varFound is True and (word != "struct" and word != "define" and word != "definetype"):
                    if word not in identifiers:
                        identifiers.append(word)
                    varFound = False
                elif word.find("[") != -1 and word.find("]") != -1:
                    continue
                else:
                    if word not in identifiers:
                        keywords.append(word)
            # Here is a conditional statement that deals with everything following the keyword forward declarations.
            # It has several conditional cases such as if word equals forward or declarations, if word equals
            # function (which means we have an identifiers name following that keyword), if we found a variable (from
            # the previous conditional), if word equals parameters (which we treat the same as function), and lastly,
            # an else statement that handles anything not covered by those conditionals.
            if (word == "forward" or phase == -4) and commentFound is False:
                phase = -4
                if word == "forward" or word == "declarations":
                    keywords.append(word)
                elif word == "function":
                    keywords.append(word)
                    varFound = True
                elif varFound is True and word != "function":
                    identifiers.append(word)
                    varFound = False
                elif word == "parameters":
                    varFound = True
                    keywords.append(word)
                elif word.find(",") == len(word) - 1 and len(word) != 1:
                    varFound = True
                    keywords.append(word[:len(word) - 1])
                else:
                    if word not in identifiers and word != ",":
                        keywords.append(word)
            # Here is a conditional statement that deals with everything following the keyword global declarations.
            # It has several conditional cases such as if word equals variables (which means everything underneath
            # describes a variable), word equals define, and we are under variables (which means a variable name is up
            # next), a statement that deals with the variable names, if word equals constants (which means everything
            # underneath describes a constant), word equals define, and we are under constants (which means a constant
            # name is up next), a statement that deals with constant names, a statement that denotes we are leaving
            # global declarations by detecting if word equals implementations, and lastly an else statements that
            # deals with anything else that does not fall under the previously mentioned conditionals.
            if (word == "global" or phase == -5) and commentFound is False:
                phase = -5
                if word == "variables":
                    globalVar = True
                    globalCon = False
                    keywords.append(word)
                elif globalVar is True and word == "define":
                    varFound = True
                    keywords.append(word)
                elif varFound is True and word != "define":
                    varFound = False
                    identifiers.append(word)
                elif word == "constants":
                    globalCon = True
                    keywords.append(word)
                elif globalCon is True and word == "define":
                    conFound = True
                    keywords.append(word)
                elif conFound is True and word != "define":
                    conFound = False
                    constants.append(word)
                elif word == "implementations":
                    globalCon = False
                    phase = 0
                else:
                    if word != "=" and word.isdigit() is False:
                        keywords.append(word)
            # Here is a conditional statement that deals with everything following the keyword symbol. It has two
            # conditions, dealing with the word symbol itself, and dealing with the variable name following symbol.
            if word == "symbol" or phase == -2:
                phase = -2
                if word == "symbol":
                    keywords.append(word)
                    varFound = True
                if varFound is True and word != "symbol":
                    constants.append(word)
                    varFound = False
                    phase = 0
            # Here is a conditional statement that deals with everything following the keyword import. It has two
            # conditions, dealing with the import keyword itself and dealing with the following variable name.
            if (word == "import" or phase == -1) and commentFound is False:
                varFound = True
                phase = -1
                if word == "import":
                    keywords.append(word)
                else:
                    identifiers.append(word[1:len(word) - 1])
                    varFound = False
                    phase = 0
            # Here is a conditional statement that deals with everything following the keyword implementations. It
            # has several conditional statements such as dealing with the keyword implementations itself,
            # dealing with the keyword variables (which denotes that we have left the implementations block),
            # dealing with the keyword function (which denotes a variable name is up next), dealing with the variable
            # name itself, and lastly, an else statements that deals with anything that is not applicable to the
            # previously mentioned statements.
            if (word == "implementations" or phase == 1) and commentFound is False:
                phase = 1
                if word == "implementations":
                    keywords.append(word)
                elif word == "variables":
                    phase = 0
                elif word == "function":
                    keywords.append(word)
                    varFound = True
                elif varFound is True and word != "function":
                    if word not in identifiers:
                        identifiers.append(word)
                    varFound = False
                else:
                    if word not in identifiers and word != "begin":
                        keywords.append(word)
            # Here is a conditional statement that deals with everything following the keyword variables. It has
            # several conditional statement within it such as if the word is variables, if the word is begin (which
            # symbolizes we have left the variables block), if the word is define (which symbolizes a variable name
            # is up next), dealing with the variable name itself, and lastly, an else statements that deals with
            # anything that does not fall under the previously mentioned conditionals.
            if (word == "variables" or phase == 2) and commentFound is False and phase != 5:
                phase = 2
                if word == "variables":
                    keywords.append(word)
                elif word == "begin":
                    phase = 0
                elif word == "define":
                    keywords.append(word)
                    varFound = True
                elif varFound is True and word != "define":
                    identifiers.append(word)
                    varFound = False
                else:
                    if word not in identifiers:
                        keywords.append(word)
            # Here is a conditional statement that deals with everything following the keyword begin. It has several
            # conditional statements within it such as if the word equals begin, if the word equal endfun (which
            # denotes we are leaving the begin block), if the word equals display (which means a string is following
            # and we used some if statements within that to detect and get the string without any other special
            # characters surrounding it), if the word equals an operator, if the word is a digit, and lastly,
            # an else statement that deals with anything that does not fall under the previously mentioned
            # conditional statements.
            if (word == "begin" or phase == 3) and commentFound is False:
                phase = 3
                if word == "begin":
                    keywords.append(word)
                elif word == "endfun":
                    keywords.append(word)
                    phase = 0
                elif word == "display":
                    keywords.append(word)
                    stringFound = True
                elif stringFound is True and word != "display":
                    if word.find('"') == 0 and word.find(",") == -1 and len(word) > 1:
                        tempString += word[1:]
                    if word.find('"') == -1:
                        tempString = tempString + " " + word
                    if word.find('"') == 0 and len(word) == 1:
                        strings.append(tempString)
                        tempString = ""
                        stringFound = False
                    if word.find('"') == len(word) - 1 and len(word) != 1:
                        tempString = tempString + " " + word[:len(word) - 1]
                        strings.append(tempString)
                        tempString = ""
                        stringFound = False
                    if (word.find('"') == len(word) - 2 or word.find('"') == len(word) - 1) and word.find(",") != -1:
                        strings.append(tempString)
                        tempString = ""
                        stringFound = False
                elif word == "+" or word == "-" or word == "/" or word == "*" or word == "(" or word == ")" or word == "=":
                    operators.append(word)
                    continue
                elif word.find("(") != -1:
                    continue
                elif word.isdigit():
                    continue
                elif word.find(".") != -1:
                    identifiers.append(word)
                else:
                    if word not in identifiers and word not in constants:
                        keywords.append(word)
            # Here is a conditional statement that deals with everything following the keyword functions that is not
            # declared underneath another keyword codeblock. It has three conditional statements that deal with the
            # words function, is, and the variable name following function.
            if (word == "function" and phase == 0) or phase == 4:
                phase = 4
                if word == "function":
                    varFound = True
                    keywords.append(word)
                if varFound is True and word != "function":
                    if word not in identifiers:
                        identifiers.append(word)
                    varFound = False
                if word == "is":
                    keywords.append(word)
                    phase = 0
                    continue
        commentFound = False
    i = 0
    # These are our print statements that prints out our arrays that contain our scanned data.
    print("Keywords are: ")
    for word in keywords:
        print(word, end=", ")
        i = i + 1
        if i % 10 == 0:
            i = 0
            print("\t")
    i = 0
    print("\n")
    print("Identifiers are: ")
    for word in identifiers:
        print(word, end=", ")
        i = i + 1
        if i % 10 == 0:
            i = 0
            print("\t")
    i = 0
    print("\n")
    print("Operators are: ")
    for word in operators:
        print(word, end=", ")
        i = i + 1
        if i % 10 == 0:
            i = 0
            print("\t")
    i = 0
    print("\n")
    print("Constants are: ")
    for word in constants:
        print(word, end=", ")
        i = i + 1
        if i % 10 == 0:
            i = 0
            print("\t")
    i = 0
    print("\n")
    print("Strings are: ")
    for word in strings:
        print(word, end=", ")
        i = i + 1
        if i % 10 == 0:
            i = 0
            print("\t")
    key_file = open("linked_keywords.json", "w")
    json.dump(keywords, key_file)
    ident_file = open("linked_identifiers.json", "w")
    json.dump(identifiers, ident_file)
    oper_file = open("linked_operators.json", "w")
    json.dump(operators, oper_file)
    con_file = open("linked_constants.json", "w")
    json.dump(constants, con_file)