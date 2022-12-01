'''
Created on Nov 28, 2022

@author: Antonio Balanzategui, antbalanzategui
'''
import hashlib 
from time import time

tFile = open("common-passwords-win.txt")
contents = tFile.readlines()
i = 0
listOfWords = ""
d = {}
while i < len(contents):
    
    concat = ""
    concat += str(i+1)
    concat += ": "
    concat += contents[i]
    if (i != len(contents) - 1):
        concat += ", "
    listOfWords += concat
    i = i + 1

listOfWords += ""
result = dict((b.strip(), int(a.strip()))  
    for a, b in (element.split(':')
        for element in listOfWords.split(', '))) 

timeArray256 = []
timeArray512 = []
 

def requestInput():
    userInput = input("Please Enter a Password to Crack: ")
    if (validateInput(userInput, result) == True):
        print("SHA 256: "+hashInput_256(userInput))
        print("SHA 512: "+hashInput_512(userInput))
        time = passwordCrack_256(result, userInput)
        time2 = passwordCrack_512(result, userInput)
        timeArray256.append(time)
        timeArray512.append(time2)
        print("Time for SHA256: ", time)
        print("Time for SHA512: ", time2)
        return userInput
    elif (userInput == 'q'):
        print("Exitted Console")
    else:
        print("Invalid Input!")
    return userInput

def validateInput(uInput, d):
    inputLength = len(uInput)
    i = 0
    counter = 0
    limitCounter = 0
    validationString = ""
    while (i < inputLength):
        validationString += uInput[i]
        if (d.get(validationString) != None):
            counter = counter - (len(validationString) - 1)
            validationString = ""
            limitCounter = limitCounter + 1
        else:
            counter = counter + 1
        i = i + 1
    return counter == 0 and limitCounter < 4

def hashInput_256(uInput):
    hashed_string = hashlib.sha256(uInput.encode('utf-8')).hexdigest()
    return hashed_string

def hashInput_512(uInput):
    hashed_string = hashlib.sha512(uInput.encode('utf-8')).hexdigest()
    return hashed_string

def passwordCrack_256(result, userInput):
    start = time()
    user256 = hashInput_256(userInput)
    for i in result:
        holder = i
        check256 = hashInput_256(holder)
        if (check256 == user256):
            return time() - start
        for i in result: 
            holder2 = holder + i
            check256 = hashInput_256(holder2)
            if (check256 == user256):
                return time() - start
            for i in result:
                holder3 = holder2 + i 
                check256 = hashInput_256(holder3)
                if (check256 == user256):
                    return time() - start
                else:
                    holder3 = ""
    
        
def passwordCrack_512(result, userInput):
    start = time()
    user512 = hashInput_512(userInput)
    for i in result:
        holder = i
        check512 = hashInput_512(holder)
        if (check512 == user512):
            return time() - start
        for i in result: 
            holder2 = holder + i
            check512 = hashInput_512(holder2)
            if (check512 == user512):
                return time() - start
            for i in result:
                holder3 = holder2 + i 
                check512 = hashInput_512(holder3)
                if (check512 == user512):
                    return time() - start
                else:
                    holder3 = ""
        

selectedString = ""
while (selectedString != 'q'):
    selectedString = requestInput()

result_swap = {v: k for k, v in result.items()}
print(timeArray256)
print(timeArray512)



