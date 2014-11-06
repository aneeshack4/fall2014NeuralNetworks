import time
import praw

r = praw.Reddit('PRAW related-question monitor by u/_Daimon_ v 1.0.'
                'Url: https://praw.readthedocs.org/en/latest/'
                'pages/writing_a_bot.html')
r.login()
already_done = []

prawWords = ['praw', 'reddit_api', 'mellort']
mapDict = {}
# while True:
subreddit = r.get_subreddit('learnpython')
for submission in subreddit.get_hot(limit=100):
    op_text = submission.selftext.lower()
    has_praw = any(string in op_text for string in prawWords)
    # Test if it contains a PRAW-related question
    if submission.id not in already_done and has_praw:
        msg = '[PRAW related thread](%s)' % submission.short_link
        r.send_message('_Daimon_', 'PRAW Thread', msg)
        already_done.append(submission.id)
    title = submission.title
    #print(title)
    #print submission.ups
    print submission.score #ups - downvotes
    words = title.split()
    print words
    wordsDict = []
    for word in words:
    	wordsDict.append(word)
    mapDict[submission.title] = words;
    # time.sleep(1800)
for key in mapDict:
	print key, 'bag of words in this title: ', mapDict[key]
	print "/n"