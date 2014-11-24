import time
import praw
import cPickle
import gzip
import numpy
import scipy

import theano
import theano.tensor as T

r = praw.Reddit('PRAW related-question monitor by u/_Daimon_ v 1.0.'
                'Url: https://praw.readthedocs.org/en/latest/'
                'pages/writing_a_bot.html')
r.login()
already_done = []

prawWords = ['praw', 'reddit_api', 'mellort']

subreddit = r.get_subreddit('news')

word_count = {}

outerList = []
outerTopList = []
outerMiddleList = []
outerBottomList = []

titles = []

title_scores = []

top = [] #submissions with a score of more than 1000
middle = [] #submissions with a score between 1000 and 100
bottom = [] #submissions with a score less than or equal to 100 

top_title_dict = {}
middle_title_dict = {}
bottom_title_dict = {}

for submission in subreddit.get_hot(limit=1000):
    op_text = submission.selftext.lower()
    has_praw = any(string in op_text for string in prawWords)
    # Test if it contains a PRAW-related question
    if submission.id not in already_done and has_praw:
        msg = '[PRAW related thread](%s)' % submission.short_link
        r.send_message('_Daimon_', 'PRAW Thread', msg)
        already_done.append(submission.id)
    titles.append(submission.title) #changed from str(title).lower()
    title = submission.title.split()
    for t in title:
        word_count[t] = 0
        #word_count[str(t).lower()] = 0
    title_scores.append(submission.score)
    if (submission.score >= 500):
        top.append(submission.title)
    elif(submission.score < 500 and submission.score >= 50):
        middle.append(submission.title)
    else:
        bottom.append(submission.title)

title_word_counts = {}

#print str(title_scores)

#print str(sorted(word_count)) + "\n"

#all titles 
for title in titles:
    title_dict = word_count.copy()
    words = title.split()
    for word in words:
        title_dict[word]+=1
        #title_dict[str(word).lower()]+=1
    title_count = []
    for key in sorted(title_dict):
        title_count.append(title_dict[key])
    #print "Title: " + title
    #print "Outer List:\n" + str(title_count) + "\n"
    outerList.append(title_count)
    title_word_counts[title] = title_dict

#top submissions, middle submissions, bottom submissions
for title in top:
    top_title_dict = word_count.copy()
    words = title.split()
    for word in words:
        top_title_dict[word]+=1
        #top_title_dict[str(word).lower()]+=1
    top_title_count = []
    for key in sorted(top_title_dict):
        top_title_count.append(top_title_dict[key])
    #print "Title: " + title
    #print "Outer List:\n" + str(top_title_count) + "\n"
    outerTopList.append(top_title_count)

for title in middle:
    middle_title_dict = word_count.copy()
    words = title.split()
    for word in words:
        middle_title_dict[word]+=1
        #middle_title_dict[str(word).lower()]+=1
    middle_title_count = []
    for key in sorted(middle_title_dict):
        middle_title_count.append(middle_title_dict[key])
    #print "Title: " + title
    #print "Outer List:\n" + str(middle_title_count) + "\n"
    outerMiddleList.append(middle_title_count)

for title in bottom:
    bottom_title_dict = word_count.copy()
    words = title.split()
    for word in words:
        bottom_title_dict[word]+=1
        #bottom_title_dict[str(word).lower()]+=1
    bottom_title_count = []
    for key in sorted(bottom_title_dict):
        bottom_title_count.append(bottom_title_dict[key])
    #print "Title: " + title
    #print "Outer List:\n" + str(bottom_title_count) + "\n"
    outerBottomList.append(bottom_title_count)

print len(outerTopList)
print len(outerMiddleList)
print len(outerBottomList)

# training_set = []
# training_classification = []

# validation_set = []
# validation_classification = []

# test_set = []
# test_classification = []

whole_thing_set = [[],[],[]]
whole_thing_classification = [[],[],[]]

listNum = 0
for i in range(0, max(len(outerTopList), len(outerBottomList), len(outerMiddleList))) :
    listNum = listNum % 3

    if i < len(outerTopList) : 
        whole_thing_set[listNum].append(outerTopList[i])
        whole_thing_classification[listNum].append(2)

    if i < len(outerMiddleList) :
            whole_thing_set[listNum].append(outerMiddleList[i])
            whole_thing_classification[listNum].append(1)

    if i < len(outerBottomList) :
        whole_thing_set[listNum].append(outerBottomList[i])
        whole_thing_classification[listNum].append(0)

    listNum = listNum + 1

# saveMatrix = []
# saveMatrix.append((theano.shared(numpy.array(whole_thing_set[0])), theano.shared(numpy.array(whole_thing_classification[0]))))
# saveMatrix.append((theano.shared(numpy.array(whole_thing_set[1])), theano.shared(numpy.array(whole_thing_classification[1]))))
# saveMatrix.append((theano.shared(numpy.array(whole_thing_set[2])), theano.shared(numpy.array(whole_thing_classification[2]))))


saveMatrix = []
saveMatrix.append((whole_thing_set[0], whole_thing_classification[0]))
saveMatrix.append((whole_thing_set[1], whole_thing_classification[1]))
saveMatrix.append((whole_thing_set[2], whole_thing_classification[2]))


fp = gzip.GzipFile('redditData.save.gz', 'wb')
fp.write(cPickle.dumps(saveMatrix, protocol=cPickle.HIGHEST_PROTOCOL))
fp.close()

# f = gzip.open('redditData.save.gz', 'wb')
# cPickle.dump(saveMatrix, f, protocol=cPickle.HIGHEST_PROTOCOL)
# f.close()

"""for title in title_word_counts:
    print "\n" + title
    for key in sorted(title_word_counts[title]):
        print "%s: %s" % (key, title_word_counts[title][key])"""