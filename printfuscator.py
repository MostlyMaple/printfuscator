import sys
import random
import string

formats = ["%d", "%c", "%s"]


def generateIntArgument(arguments, intValue):
    intType = random.randint(0,1)
    if intType == 0:
        intVal = random.randint(1,2147483647)
        arguments+=", " + str(intVal)
        argSize = len(str(intVal))
        intValue-=argSize
    if intType == 1:
        intVal = random.randint(1,2147483647)
        arguments+=", " + str(hex(intVal))
        argSize = len(str(intVal))
        intValue-=argSize
    return intValue, arguments

def generateCharArgument(arguments, intValue):
    charKey = random.choice(string.ascii_letters)
    argSize = 1
    arguments+=", \'" + str(charKey) + "\'";
    intValue-=argSize;
    return intValue, arguments

def generateStringArgument(arguments, intValue):
    stringType = random.randint(0,1)
    if stringType == 0:
        argSize = random.randint(1,10);
        randString = "";
        for i in range(argSize):
            randString+=random.choice(string.ascii_letters);
        arguments+=", \"" + str(randString) + "\"";
        intValue-=argSize;
    if stringType == 1:
        argSize = random.randint(1,10);
        randString = "";
        for i in range(argSize):
            randString+=random.choice(string.ascii_letters)
        byteString = bytes(randString, 'utf-8')
        arguments+= ", \""
        for c in byteString:
            arguments+= hex(c).replace("0x","\\x")
        arguments+= "\""
        intValue-=argSize
    return intValue, arguments

def padLastValuesWithString(arguments, intValue, formatString):
    argSize = intValue
    formatString+=formats[2]
    randString = "";
    for i in range(argSize):
        randString+=random.choice(string.ascii_letters);
    arguments+=", \"" + str(randString) + "\"";
    intValue-=argSize;
    return intValue, arguments, formatString

def addPercentNArgument(arguments, intName, formatString):
    formatString+='\x1b[1;31;40m' + "%n" + '\x1b[0m'
    arguments+=", " + '\x1b[1;31;40m' + "&" + intName + '\x1b[0m'
    return arguments, formatString

def main():
    numArgs = len(sys.argv)
    if numArgs < 2:
        print("USAGE:\npython printfuscator.py variableName integerValue garbageValue")
        print("\tvariableName: The name of the variable the printf will store the int value in")
        print("\tintegerValue: (Integer) The value to store inside the variable")
        print("\tgarbageValue: (Integer) The amount of random values to print after the %n")
        exit()
    try:
        varName = sys.argv[1]
    except:
        print("Error reading in variableName!")
        exit()
    try:
        intValue = int(sys.argv[2])
    except:
        print("Error reading in integerValue!")
        exit()
    try:
        garbage = int(sys.argv[3])
    except:
        print("No garbage specified - Using default 0!\n")
        garbage = 0
    formatString = ""
    arguments = ""

    while (intValue > 10):
        nextArgType = random.randint(0,2);
        formatString+=formats[nextArgType]
        if (nextArgType == 0):
            intValue, arguments = generateIntArgument(arguments, intValue)
        elif (nextArgType == 1):
            intValue, arguments = generateCharArgument(arguments, intValue)
        elif(nextArgType == 2):
            intValue, arguments = generateStringArgument(arguments, intValue)
    
    intValue, arguments, formatString = padLastValuesWithString(arguments, intValue, formatString)
    arguments, formatString = addPercentNArgument(arguments, varName, formatString)

    while (garbage > 10):
        nextArgType = random.randint(0,2);
        formatString+=formats[nextArgType]
        if (nextArgType == 0):
            garbage, arguments = generateIntArgument(arguments, garbage)
        elif (nextArgType == 1):
            garbage, arguments = generateCharArgument(arguments, garbage)
        elif(nextArgType == 2):
            garbage, arguments = generateStringArgument(arguments, garbage)

    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
    print("int " + varName + ";")
    print("fprintf(stdin, \"" + formatString + "\"" + arguments + ");")
    print("printf(\"%d\", " + varName + ");")
    print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

main()