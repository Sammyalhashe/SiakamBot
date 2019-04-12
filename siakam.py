import praw
from praw.models import MoreComments
import os
import re

###############################################################################
reply = """
Woops! Looks like you mispelled Pascal's name! It is spelled *Siakam*
"""


###############################################################################
def printDetails(submission):
    print("Title: ", submission.title)
    # print("Text: ", submission.selftext)
    print("Score: ", submission.score)
    print("---------------------------------\n")


def checkPresence(submission, subList, commentList):
    mispells = ["siakim", "sakam", "sakiam"]
    title = False
    comments = False
    for mispell in mispells:
        if re.search(mispell, submission.title, re.IGNORECASE):
            title = True
            submission.reply(reply)
            subList.append(submission.id)
            print("Post {0} replied to\n".format(submission.id))
            print(submission.selftext.encode())
        for comment in submission.comments.list():
            if comment.id not in commentList:
                # print(type(comment))
                if isinstance(comment, MoreComments):
                    continue
                # print(comment.body)
                if re.search(mispell, comment.body, re.IGNORECASE):
                    comments = True
                    comment.reply(reply)
                    commentList.append(comment.id)
                    print("Comment {0} replied to\n".format(comment.id.encode()))
                    print(comment.body.encode())
    return title, comments


###############################################################################
# subreddit = "pythonforengineers"
# subreddit = "torontoraptors"
subreddits = ["nba", "torontoraptors"]
# subreddit = "nba"

reddit = praw.Reddit('siakam')

for subreddit in subreddits:
    sub = reddit.subreddit(subreddit)

    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            first = f.read()
            second = first.split('\n')
            posts_replied_to = list(filter(None, second))

    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            first = f.read()
            second = first.split('\n')
            comments_replied_to = list(filter(None, second))

###############################################################################
    for submission in sub.hot(limit=100):
        if submission.id not in posts_replied_to:
            printDetails(submission)
            checkPresence(submission, posts_replied_to, comments_replied_to)

###############################################################################
    with open('posts_replied_to.txt', 'w') as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
        f.close()

    with open('comments_replied_to.txt', 'w') as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")
        f.close()
