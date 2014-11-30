import sys

#gets the input title from the command line
sys.argv.pop(0)
title = sys.argv

#reads in a list of words from an input file (changes whenever reddit bot is run)
file = open('words.txt', 'r')
words = file.read().split()

wordList = {}

#creates a list, titleCount, of the number of occurrences of each word in the title
for word in words:
    wordList[word] = 0
for word in title:
	if word in wordList:
		wordList[word] += 1
	else:
		wordList[word] = 1
titleCount = []
for key in sorted(wordList):
    titleCount.append(wordList[key])