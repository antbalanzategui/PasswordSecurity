'''
Created on Nov 28, 2022

@author: Antonio Balanzategui, antbalanzategui
'''
import hashlib 
from time import time
from collections import deque
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np





sys.setrecursionlimit(5000)

tFile = open("common-passwords-win.txt")
contents = tFile.readlines()
i = 0
listOfWords = ""
d = {}
wordList = []
inputList = []
numberOfGuess = []
# While loop to create a string of all words within
# the read text file
while i < len(contents):
    
    concat = ""
    concat += str(i+1)
    concat += ": "
    concat += contents[i]
    wordList.append(contents[i].replace('\n', ""))
    if (i != len(contents) - 1):
        concat += ", "
    listOfWords += concat
    i = i + 1

listOfWords += ""
# Uses earlier string created to 
# initialize a dictionary containing all words
result = dict((b.strip(), int(a.strip()))  
    for a, b in (element.split(':')
        for element in listOfWords.split(', '))) 

# Dictionary Swap
result_swap = {v: k for k, v in result.items()}
#Array Objects which will hold times 
timeArray256 = []
timeArray512 = []

def recExtras(l, theSum):
    if (l == 3):
        return theSum + 12
    else:
        theSum = theSum + l * 2
        return recExtras(l - 1, theSum)

def emptyQueue(lister):
    i = 0 
    queue = deque()
    while i < len(lister):
        queue.append("")
        i = i + 1
    return queue


queue = emptyQueue(wordList)
extra = recExtras(len(wordList), 0)
 
# Void method to requestInput from a user, responsible for 
# entire program, encapsulates all other methods
def requestInput():
    userInput = input("Please Enter a Password to Crack: ")
    if (recValidateInput(userInput, result, 0, 0, 0, "") == True):
        
        print("SHA 256: "+hashInput_256(userInput))
        print("SHA 512: "+hashInput_512(userInput))
        inputList.append(userInput)
        start = time()
        numberOfGuess.append(recCombos512(wordList, emptyQueue(wordList), 0, 3, 0, 0, userInput, extra))
        newTime = time() - start
        timeArray512.append(newTime)
        recCombos512(wordList, emptyQueue(wordList), 0, 3, 0, 0, userInput, extra)
        newTime2 = time() - start
        timeArray256.append(newTime2)
        print("Time for SHA256: ", newTime)
        print("Time for SHA512: ", newTime2)
        return userInput
    elif (userInput == 'q'):
        print("Exitted Console")
    else:
        print("Invalid Input!")
    return userInput
# Method to ensure a user input is valid 
#def validateInput(uInput, d):
    #inputLength = len(uInput)
    #i = 0
    #counter = 0
    #limitCounter = 0
    #validationString = ""
    #while (i < inputLength):
        #validationString += uInput[i]
        #if (d.get(validationString) != None):
            #counter = counter - (len(validationString) - 1)
            #validationString = ""
            #limitCounter = limitCounter + 1
        #else:
            #counter = counter + 1
        #i = i + 1
    #return counter == 0 and limitCounter < 4

#Method to recursively validate an input
def recValidateInput(uInput, d, i, counter, limitCounter, validationString):
    if i == len(uInput):
        return counter == 0 and limitCounter < 4
    else:
        validationString += uInput[i]
        if (d.get(validationString) != None):
            return recValidateInput(uInput, d, i + 1, counter - (len(validationString) - 1), limitCounter + 1, "")
        else:
            return recValidateInput(uInput, d, i + 1, counter + 1, limitCounter, validationString)
            
    
    

# Method that Hashes userInput via SHA256
def hashInput_256(uInput):
    hashed_string = hashlib.sha256(uInput.encode('utf-8')).hexdigest()
    return hashed_string
# Method that Hashes userInput via SHA512
def hashInput_512(uInput):
    hashed_string = hashlib.sha512(uInput.encode('utf-8')).hexdigest()
    return hashed_string
# Method to crack the SHA256 encryption, 
# uses for loops, to iterate from all combinations of words possible
# will get all combination of "aaa..." possible before reaching "abc"
#def passwordCrack_256(result, userInput):
    #start = time()
    #user256 = hashInput_256(userInput)
    #for i in result:
        #holder = i
        #check256 = hashInput_256(holder)
        #if (check256 == user256):
            #return time() - start
        #for i in result: 
            #holder2 = holder + i
            #check256 = hashInput_256(holder2)
            #if (check256 == user256):
                #return time() - start
            #for i in result:
                #holder3 = holder2 + i 
                #check256 = hashInput_256(holder3)
                #if (check256 == user256):
                    #return time() - start
                #else:
                    #holder3 = ""
    
# Method to crack the SHA512 encryption, 
# uses for loops, to iterate from all combinations of words possible
# will get all combination of "aaa..." possible before reaching "abc"        
#def passwordCrack_512(result, userInput):
    #start = time()
    #user512 = hashInput_512(userInput)
    #for i in result:
        #holder = i
        #check512 = hashInput_512(holder)
        #if (check512 == user512):
            #return time() - start
        #for i in result: 
            #holder2 = holder + i
            #check512 = hashInput_512(holder2)
            #if (check512 == user512):
                #return time() - start
            #for i in result:
                #holder3 = holder2 + i 
                #check512 = hashInput_512(holder3)
                #if (check512 == user512):
                    #return time() - start
                #else:
                    #holder3 = ""
        

def receiveMaxCombinations(wordList, k):
    i = 1
    maxCount = 0
    while i <= k:
        maxCount =+ len(wordList)**i
        i = i + 1
    return maxCount

        
#QUEUE OF LENGTH NEEDED WITH '' empty spots
def recCombos512(listOfWords, queue, i, k, limit, counter, userInput, extra):
    wordInQueue = queue.popleft()
    print("Word:",wordInQueue)
    currentGuess = str(wordInQueue) + listOfWords[i]
    shaGUESS = hashInput_512(currentGuess)
    shaInput = hashInput_512(userInput)
    print("STR:", currentGuess)
    j = 0
    while j < len(listOfWords):
        queue.append(currentGuess)
        j = j + 1
    counter = counter + 1
    print("Counter:",counter)
    if (shaGUESS == shaInput):
        print("FOUND")
        return counter
    elif (counter == receiveMaxCombinations(listOfWords, k) + extra):
        return -1
    elif (counter == receiveMaxCombinations(listOfWords, limit + 1)):
        return recCombos512(listOfWords, queue, 0, k, limit + 1, counter, userInput, extra)
    elif (i == len(listOfWords) - 1):
        return recCombos512(listOfWords, queue, 0, k, limit, counter, userInput, extra)
    else:
        return recCombos512(listOfWords, queue, i + 1, k, limit, counter, userInput, extra)
    
def recCombos256(listOfWords, queue, i, k, limit, counter, userInput, extra):
    wordInQueue = queue.popleft()
    print("Word:",wordInQueue)
    currentGuess = str(wordInQueue) + listOfWords[i]
    shaGUESS = hashInput_256(currentGuess)
    shaInput = hashInput_256(userInput)
    print("STR:", currentGuess)
    j = 0
    while j < len(listOfWords):
        queue.append(currentGuess)
        j = j + 1
    counter = counter + 1
    print("Counter:",counter)
    if (shaGUESS == shaInput):
        print("FOUND!")
        return counter
    elif (counter == receiveMaxCombinations(listOfWords, k) + extra):
        return -1
    elif (counter == receiveMaxCombinations(listOfWords, limit + 1)):
        return recCombos256(listOfWords, queue, 0, k, limit + 1, counter, userInput, extra)
    elif (i == len(listOfWords) - 1):
        return recCombos256(listOfWords, queue, 0, k, limit, counter, userInput, extra)
    else:
        return recCombos256(listOfWords, queue, i + 1, k, limit, counter, userInput, extra)

# Prompts user to keep entering passwords to crack,
# until the user prompts the letter q

selectedString = ""
while (selectedString != 'q'):
    selectedString = requestInput()
    


print(inputList)
print(timeArray256)
print(timeArray512)
print(numberOfGuess)

#plt.plot(timeArray256, numberOfGuess)
#index = 0
#while index < len(timeArray256):
    #plt.plot(timeArray256[index], numberOfGuess[index])
    #plt.annotate(inputList[index], xy=(timeArray256[index], numberOfGuess[index]), xytext=(timeArray256[index], numberOfGuess[index] + 50*index),
            #arrowprops=dict(facecolor='black', shrink=0.01))
    #index = index + 1
    
#plt.ylabel("Number of Searches")
#plt.xlabel("Time for Word Guess")
#plt.suptitle("SHA256:")
#plt.show()

#switch = input("")


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
x = timeArray256
y = numberOfGuess

l, = plt.plot(x, y, lw=2)
ax.title.set_text('SHA 256')
index = 0
#while index < len(timeArray256):
    #plt.plot(timeArray256[index], numberOfGuess[index])
    #plt.annotate(inputList[index], xy=(timeArray256[index], numberOfGuess[index]), xytext=(timeArray256[index], numberOfGuess[index] + 50*index),
            #arrowprops=dict(facecolor='black', shrink=0.01))
    #index = index + 1
    


class Index(object):
    ind = 0
    global funcs # used so yu can access local list, funcs, here
    def next(self, event):
        self.ind += 1 
        i = self.ind %(len(funcs))
        x,y,name = funcs[i]() # unpack tuple data
        l.set_xdata(x) #set x value data
        l.set_ydata(y) #set y value data
        ax.title.set_text(name) # set title of graph
        plt.draw()

    def prev(self, event):
        self.ind -= 1 
        i  = self.ind %(len(funcs))
        x,y, name = funcs[i]() #unpack tuple data
        l.set_xdata(x) #set x value data
        l.set_ydata(y) #set y value data
        ax.title.set_text(name) #set title of graph
        plt.draw()

def plot1():
    x = timeArray256
    y = numberOfGuess
    return (x,y,"SHA256")

def plot2():
    x = timeArray512
    y = numberOfGuess
    return (x,y,"SHA512")


funcs = [plot1, plot2] # functions in a list so you can interate over
callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)
index = 0
plt.show()





