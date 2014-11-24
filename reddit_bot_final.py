import time
import praw

r = praw.Reddit('PRAW related-question monitor by u/_Daimon_ v 1.0.'
                'Url: https://praw.readthedocs.org/en/latest/'
                'pages/writing_a_bot.html')
r.login()
already_done = []

prawWords = ['praw', 'reddit_api', 'mellort']

subreddit = r.get_subreddit('learnpython')

word_count = {}

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

top_training_dict = {}
middle_training_dict = {}
bottom_training_dict = {}

top_validation_dict = {}
middle_validation_dict = {}
bottom_training_dict = {}

top_testing_dict = {}
middle_validation_dict = {}
bottom_training_dict = {}

for submission in subreddit.get_hot(limit=1000):
    op_text = submission.selftext.lower()
    has_praw = any(string in op_text for string in prawWords)
    # Test if it contains a PRAW-related question
    if submission.id not in already_done and has_praw:
        msg = '[PRAW related thread](%s)' % submission.short_link
        r.send_message('_Daimon_', 'PRAW Thread', msg)
        already_done.append(submission.id)
    titles.append(str(submission.title))
    title = submission.title.split()
    for t in title:
        word_count[str(t).lower()] = 0
    title_scores.append(submission.score)
    if (submission.score > 1000):
        top.append(submission.title)
    elif(submission < 1000 and submission > 100):
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
        title_dict[str(word).lower()]+=1
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
        top_title_dict[str(word).lower()]+=1
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
        middle_title_dict[str(word).lower()]+=1
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
        bottom_title_dict[str(word).lower()]+=1
    bottom_title_count = []
    for key in sorted(bottom_title_dict):
        bottom_title_count.append(bottom_title_dict[key])
    #print "Title: " + title
    #print "Outer List:\n" + str(bottom_title_count) + "\n"
    outerBottomList.append(bottom_title_count)

print len(top_title_dict)
print len(middle_title_dict)
print len(bottom_title_dict)

"""for title in title_word_counts:
    print "\n" + title
    for key in sorted(title_word_counts[title]):
        print "%s: %s" % (key, title_word_counts[title][key])"""