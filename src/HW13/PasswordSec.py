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

#Method for specific math calculation for
#combinations within recCombos
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
#Max combinations of any length list
def receiveMaxCombinations(wordList, k):
    i = 1
    maxCount = 0
    while i <= k:
        maxCount =+ len(wordList)**i
        i = i + 1
    return maxCount

        
#Recursive method to use crack password given by user
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

#Recursive method to use crack password given by user
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


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
x = timeArray256
y = numberOfGuess

l, = plt.plot(x, y, lw=2)
ax.title.set_text('SHA 256')
index = 0

# Class creation in order to implement Swapping   
class Index(object):
    ind = 0
    global funcs 
    def SHA512(self, event):
        self.ind += 1 
        i = self.ind %(len(funcs))
        x, y, name = funcs[i]() 
        l.set_xdata(x) 
        l.set_ydata(y) 
        ax.title.set_text(name)
        ax.set(xlabel = "Seconds", ylabel = "Combos Attempted")
        numOfItems = 0
        while numOfItems < len(timeArray256):
            ax.annotate(inputList[numOfItems], xy=(timeArray512[numOfItems], numberOfGuess[numOfItems]), xytext=(timeArray512[numOfItems], numberOfGuess[numOfItems] - numOfItems*100),
                        arrowprops=dict(facecolor='black', shrink=0.05),)
            numOfItems = numOfItems + 1
        plt.draw()
    def SHA256(self, event):
        self.ind += 1 
        i = self.ind %(len(funcs))
        x, y, name = funcs[i]() 
        l.set_xdata(x) 
        l.set_ydata(y) 
        ax.title.set_text(name)
        ax.set(xlabel = "Seconds", ylabel = "Combos Attempted")
        numOfItems = 0
        while numOfItems < len(timeArray256):
            ax.annotate(inputList[numOfItems], xy=(timeArray256[numOfItems], numberOfGuess[numOfItems]), xytext=(timeArray256[numOfItems], numberOfGuess[numOfItems] - numOfItems*100),
                        arrowprops=dict(facecolor='black', shrink=0.05),)
            numOfItems = numOfItems + 1
        plt.draw()
#PLOT for 256 SHA
def SHA256PLOT():
    x = timeArray256
    y = numberOfGuess
    return (x,y, "SHA256")
#Plot for 512 SHA
def SHA512PLOT():
    x = timeArray512
    y = numberOfGuess
    return (x,y,"SHA512")
#SWAP functionality below
funcs = [SHA256PLOT, SHA512PLOT]
callback = Index()
axSHA512 = plt.axes([0.20, 0.04, 0.20, 0.04])
axSHA256 = plt.axes([0.60, 0.04, 0.20, 0.04])
bSHA256 = Button(axSHA256, 'SHA256')
bSHA256.on_clicked(callback.SHA256)
bSHA512 = Button(axSHA512, 'SHA512')
bSHA512.on_clicked(callback.SHA512)
index = 0
plt.show()