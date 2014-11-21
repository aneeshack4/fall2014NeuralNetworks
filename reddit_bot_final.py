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

titles = []

for submission in subreddit.get_hot(limit=10):
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
        word_count[str(t)] = 0

title_word_counts = {}

for title in titles:
    title_dict = word_count.copy()
    words = title.split()
    for word in words:
        title_dict[str(word)]+=1
    title_word_counts[title] = title_dict

for title in title_word_counts:
    print "\n" + title
    for key in sorted(title_word_counts[title]):
        print "%s: %s" % (key, title_word_counts[title][key])