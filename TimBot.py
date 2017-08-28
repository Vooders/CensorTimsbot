import praw
import re
import logging
import shelve

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Start of program')
reddit=praw.Reddit('TimBot')
logging.info('Initiated TimBot')
subreddit=reddit.subreddit("hellointernet")

with open("post_IDs.txt","w+") as f:
    postIDs=f.read().split('\n')
try:
    logging.info('Retrieved post IDs')

    naughtyCheck=re.compile(r'''(naughty)''',re.IGNORECASE)
    logging.info('Compiled regex for naughty')

    postComment="I noticed you used bad language in your post.\n Please use n*aughty to censor it.\n\n\n ^^I ^^am ^^TimBot"

    while True:
        for post in subreddit.new(limit=15):
            logging.info('Checking next post,'+str(post.id))
            if post.id not in postIDs:
                mo1=naughtyCheck.search(post.title)
                mo2=naughtyCheck.search(post.selftext)
                if mo1 != None or mo2 != None:
                    post.reply(postComment)
                    logging.info('Found bad post, replied to a post by '+str(post.author)+' id:'+str(post.id))
                    postIDs.append(post.id)

                    
        for post in subreddit.hot(limit=30):
            post.comments.replace_more(limit=0) #replace all more comments instances
            comment_queue = post.comments[:] #retrieve all top level comments
            while comment_queue:
                
                comment = comment_queue.pop(0) #get comment
                logging.info('Checking next comment,'+str(comment.id))
                if comment.id not in postIDs:
                    mo=naughtyCheck.search(comment.body)
                    if mo != None:          #check if has bad word
                        comment.reply(postComment)
                        logging.info('Found bad comment, replied to comment by '+str(comment.author)+' id:'+str(comment.id))
                        postIDs.append(comment.id) #add comment ID to list
                comment_queue.extend(comment.replies)   #add all replies to that comment to the queue
finally:
    with open("post_IDs.txt","w+") as f:
        f.write('\n'.join(postIDs))
    






