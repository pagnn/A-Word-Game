import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

def loadWords():
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def getFrequencyDict(sequence):
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

#1: Scoring a word
def getWordScore(word, n):
    length=len(word)
    score=0
    for i in word:
        score=score+SCRABBLE_LETTER_VALUES[i]
    score=score*length
    if length==n:
        score=score+50
    return score
def displayHand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

def dealHand(n):
    hand={}
    numVowels = n / 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
#2: Update a hand by removing letters
#
def updateHand(hand, word):
    handCopy = hand.copy()
    for letter in word:
        handCopy[letter]-=1
    return handCopy



#
#3: Test word validity
#
def isValidWord(word, hand, wordList):
    handCopy=hand.copy()
    if word in wordList:
        flag=True
        for i in word:
            num = handCopy.get(i,'w')
            if num == 'w':
                flag=False
                return False
                break
            else:
                if handCopy[i]<=0:
                    return False
                else:
                    handCopy[i]=handCopy[i]-1
                    continue
        if flag:
            return True

    else:
        return False



#
# Playing a hand
#

def calculateHandlen(hand):
    c=''
    k=0
    for letter in hand.keys():
        for j in range(hand[letter]):
            c=c+letter
    k=len(c)
    return k



def playHand(hand, wordList, n):
    c=0
    score=0
    
    # As long as there are still letters left in the hand:
    while calculateHandlen(hand)>0:
        # Display the hand
        print"Current Hand:",
        displayHand(hand)
        # Ask user for input
        print 'Enter word, or a "." to indicate that you are finished:',
        word=raw_input()
        # Keep track of the total score   
        
        # If the input is a single period:
        if word=='.':
            # End the game (break out of the loop)
            if c==0:
                break
            else:
                print "Goodbye!",
                break

            
        # Otherwise (the input is not a single period):
        else:
            # If the word is not valid:
            if not(isValidWord(word, hand, wordList)):
                # Reject invalid word (print a message followed by a blank line)
                print 'Invalid word, please try again.'
                print
                continue
            # Otherwise (the word is valid):
            else:
                score=score+getWordScore(word,n)
                # Tell the user how many points the word earned, and the updated total score, in one line followed by a blank line
                print '"'+word+'"' " earned "+ str(getWordScore(word,n))+ " points. Total: "+str(score)+" points"
                print
                if calculateHandlen(hand)==len(word):
                    print"Run out of letters.",
                    
        # Update the hand 
        hand = updateHand(hand, word)
        c+=1

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    print "Total score: "+str(score)+" points."


#
#5: Playing a game
# 
def playGame(wordList):
    count=0
    prev={}
    while True:
        flag=raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if flag=='r':
            if count == 0:
                print 'You have not played a hand yet. Please play a new hand first!'
                print 
                continue
            else:
                hand=prev
                playHand(hand, wordList, HAND_SIZE)                
        elif flag=='n':
            hand=dealHand(HAND_SIZE)
            prev=hand
            count=count+1
            playHand(hand, wordList, HAND_SIZE)
        elif flag=='e':
            break
        else:
            print'Invalid command.'
            continue 
   


#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
