import sys
import time
import praw
import cPickle
import gzip

import en;

topCount = 0
topVerb = 0
topNoun = 0
topAdj = 0
topCon = 0
topOther = 0

botCount = 0
botVerb = 0
botNoun = 0
botAdj = 0
botCon = 0
botOther = 0


class Title(object):
    def __init__(self, w, isTop): #maybe add time of post, what subreddit it came from?
        self.words = w
        self.verbCount = 0;
        self.nounCount = 0;
        self.adjCount = 0;
        self.connectiveCount = 0;
        self.other = 0

        global topVerb
        global topVerb
        global topNoun
        global topAdj
        global topCon
        global topOther
        global topCount

        global botVerb
        global botNoun
        global botAdj
        global botCon
        global botOther
        global botCount

        self.count = 0
        for word in self.words:
            self.count += 1
            fixedWord = unicode(word).lower()
            if en.is_verb(fixedWord):
                if(isTop):
                    topVerb += 1
                else:
                    botVerb += 1

                self.verbCount += 1
            elif en.is_noun(fixedWord):
                if(isTop):
                    topNoun += 1
                else:
                    botNoun += 1

                self.nounCount += 1
            elif en.is_adjective(fixedWord):
                if(isTop):
                    topAdj += 1
                else:
                    botAdj += 1

                self.adjCount += 1
            elif en.is_connective(fixedWord):
                if(isTop):
                    topCon += 1
                else:
                    botCon += 1

                self.connectiveCount += 1
            else:
                if(isTop):
                    topOther += 1
                else:
                    botOther += 1

                self.other += 1
        if isTop:
            topCount += self.count
        else:
            botCount += self.count

    def getSemantics(self):
        info = []
        info.append(self.count)
        info.append(self.verbCount)
        info.append(self.nounCount)
        info.append(self.adjCount)
        info.append(self.connectiveCount)
        info.append(self.other)

        return info

#def get_network_inputs():
r = praw.Reddit('PRAW related-question monitor by u/_Daimon_ v 1.0.'
                'Url: https://praw.readthedocs.org/en/latest/'
                'pages/writing_a_bot.html')
r.login()
already_done = []

prawWords = ['praw', 'reddit_api', 'mellort']

# subreddit = r.get_subreddit('all')
subreddit = r.get_subreddit('leagueoflegends')

titles = [] #list of each post's unicode title

titleScores = [] #list of each posts's score

outerTopList = [] #list of top submission word count lists
# outerMiddleList = [] #list of top submission word count lists
outerBottomList = [] #list of top submission word count lists

top = [] #submissions with a score of more than 1000
# middle = [] #submissions with a score between 1000 and 100
bottom = [] #submissions with a score less than or equal to 100 

wordList = {} #mapping of each word in all posts to its count, used as a template

topTitleDict = {} #mapping of all words to their word count in each top post
# middleTitleDict = {} #mapping of all words to their word count in each middle post
bottomTitleDict = {} #mapping of all words to their word count in each bottom post

for submission in subreddit.get_hot(limit=1000):
    titles.append(unicode(submission.title).lower)
    # title = submission.title.split()
    # for t in title:
    #     wordList[unicode(t).lower()] = 0
    # titleScores.append(submission.score)

    title = submission.title.split()
    

    if (submission.score >= 50):
        titleInfo = Title(title, True)
        top.append(titleInfo)
    # elif(submission.score < 1000 and submission.score >= 200):
    #     middle.append(submission.title)
    else:
        titleInfo = Title(title, False)
        bottom.append(titleInfo)

# for submission in subreddit.get_rising(limit=5000):
#     titles.append(unicode(submission.title).lower)
#     # title = submission.title.split()
#     # for t in title:
#     #     wordList[unicode(t).lower()] = 0
#     # titleScores.append(submission.score)

#     title = submission.title.split()

#     if (submission.score >= 500):
#         titleInfo = Title(title, True)
#         top.append(titleInfo)
#     # elif(submission.score < 1000 and submission.score >= 200):
#     #     middle.append(submission.title)
#     else:
#         titleInfo = Title(title, False)
#         bottom.append(titleInfo)

print str(len(titles))

print("Number top: %d \t|\t Number bottom: %d" % (len(top), len(bottom)))
print("Top Av Noun: %d \t|\t Bottom Av Noun: %d" % (topNoun/len(top), botNoun/len(bottom)))
print("Top Av Verb: %d \t|\t Bottom Av Verb: %d" % (topVerb/len(top), botVerb/len(bottom))) 
print("Top Av Adj: %d \t|\t Bottom Av Adj: %d" % (topAdj/len(top), botAdj/len(bottom)))
print("Top Av Connect: %d \t|\t Bottom Av Connect: %d" % (topCon/len(top), botCon/len(bottom))) 
print("Top Av Other: %d \t|\t Bottom Av Other: %d" % (topOther/len(top), botOther/len(bottom))) 
print("Top Av Count: %d \t|\t Bottom Av Other: %d" % (topCount/len(top), botCount/len(bottom))) 




titleList = [[],[],[]]
classificationList = [[],[],[]]

listNum = 0
# for i in range(0, max(len(top), len(outerBottomList), len(outerMiddleList))):
for i in range(0, max(len(top), len(bottom))):
    listNum %= 3
    if i < len(top): 
        titleList[listNum].append(top[i].getSemantics())
        classificationList[listNum].append(1)
    # if i < len(outerMiddleList):
    #     titleList[listNum].append(outerMiddleList[i])
    #     classificationList[listNum].append(1)
    if i < len(bottom):
        titleList[listNum].append(bottom[i].getSemantics())
        classificationList[listNum].append(0)
    listNum += 1

saveMatrix = []
saveMatrix.append((titleList[0], classificationList[0]))
saveMatrix.append((titleList[1], classificationList[1]))
saveMatrix.append((titleList[2], classificationList[2]))

fp = gzip.GzipFile('funnyData.save.gz', 'wb')
fp.write(cPickle.dumps(saveMatrix, protocol=cPickle.HIGHEST_PROTOCOL))
fp.close()

# file = open('words.txt', 'w')
# for key in sorted(wordList):
#     file.write(key.encode('ascii', 'ignore').lower() + " ")