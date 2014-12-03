import sys
import time
import praw
import cPickle
import gzip

#def get_network_inputs():
r = praw.Reddit('PRAW related-question monitor by u/_Daimon_ v 1.0.'
                'Url: https://praw.readthedocs.org/en/latest/'
                'pages/writing_a_bot.html')
r.login()
already_done = []

prawWords = ['praw', 'reddit_api', 'mellort']

subreddit = r.get_subreddit('leagueoflegends')

titles = [] #list of each post's unicode title

titleScores = [] #list of each posts's score

outerTopList = [] #list of top submission word count lists
outerMiddleList = [] #list of top submission word count lists
outerBottomList = [] #list of top submission word count lists

top = [] #submissions with a score of more than 1000
middle = [] #submissions with a score between 1000 and 100
bottom = [] #submissions with a score less than or equal to 100 

wordList = {} #mapping of each word in all posts to its count, used as a template

topTitleDict = {} #mapping of all words to their word count in each top post
middleTitleDict = {} #mapping of all words to their word count in each middle post
bottomTitleDict = {} #mapping of all words to their word count in each bottom post

for submission in subreddit.get_hot(limit=150):
    titles.append(unicode(submission.title).lower)
    title = submission.title.split()
    for t in title:
        wordList[unicode(t).lower()] = 0
    titleScores.append(submission.score)
    if (submission.score >= 200):
        top.append(submission.title)
    elif(submission.score < 200 and submission.score >= 10):
        middle.append(submission.title)
    else:
        bottom.append(submission.title)

print str(len(titles))

#top submissions, middle submissions, and bottom submissions
for title in top:
    topTitleDict = wordList.copy()
    words = title.split()
    for word in words:
        topTitleDict[unicode(word).lower()] += 1
    topTitleCount = []
    for key in sorted(topTitleDict):
        topTitleCount.append(topTitleDict[key])
    outerTopList.append(topTitleCount)

for title in middle:
    middleTitleDict = wordList.copy()
    words = title.split()
    for word in words:
        middleTitleDict[unicode(word).lower()] += 1
    middleTitleCount = []
    for key in sorted(middleTitleDict):
        middleTitleCount.append(middleTitleDict[key])
    outerMiddleList.append(middleTitleCount)

for title in bottom:
    bottomTitleDict = wordList.copy()
    words = title.split()
    for word in words:
        bottomTitleDict[unicode(word).lower()] += 1
    bottomTitleCount = []
    for key in sorted(bottomTitleDict):
        bottomTitleCount.append(bottomTitleDict[key])
    outerBottomList.append(bottomTitleCount)

print len(outerTopList)
print len(outerMiddleList)
print len(outerBottomList)

titleList = [[],[],[]]
classificationList = [[],[],[]]

listNum = 0
for i in range(0, max(len(outerTopList), len(outerBottomList), len(outerMiddleList))):
    listNum %= 3
    if i < len(outerTopList): 
        titleList[listNum].append(outerTopList[i])
        classificationList[listNum].append(2)
    if i < len(outerMiddleList):
        titleList[listNum].append(outerMiddleList[i])
        classificationList[listNum].append(1)
    if i < len(outerBottomList):
        titleList[listNum].append(outerBottomList[i])
        classificationList[listNum].append(0)
    listNum += 1

saveMatrix = []
saveMatrix.append((titleList[0], classificationList[0]))
saveMatrix.append((titleList[1], classificationList[1]))
saveMatrix.append((titleList[2], classificationList[2]))

fp = gzip.GzipFile('leagueData.save.gz', 'wb')
fp.write(cPickle.dumps(saveMatrix, protocol=cPickle.HIGHEST_PROTOCOL))
fp.close()

file = open('words.txt', 'w')
for key in sorted(wordList):
    file.write(key.encode('ascii', 'ignore').lower() + " ")