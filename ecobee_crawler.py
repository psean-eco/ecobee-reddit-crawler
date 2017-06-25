import praw
import prawcore.exceptions
import reddit_constants
import requests
import slackclient

client_id = reddit_constants.client_id
client_secret = reddit_constants.client_secret
username = reddit_constants.username
password = reddit_constants.password
user_agent = reddit_constants.user_agent

def post_print(reddit):
    arr =[]
    title = "Heading:{heading}"
    upvotes = "Upvotes:{votes}"
    comments = "Comments:{comments}"
    link = "Link to Thread:{link} "
    posts = reddit.subreddit('ecobee').hot(limit=10)
    for submission in posts:
        story={}
        story["title"] = submission.title
        #print(title.format(heading=submission.title))
        story ["upvotes"] = submission.ups
        #print(upvotes.format(votes=submission.ups))
        story["link"] = "https://www.reddit.com", submission.permalink
        #print(link.format(link=submission.permalink))
        story ["totalComments"] = submission.num_comments
        #print(comments.format(comments=submission.num_comments))
        arr.append(story)

    post_to_slack(arr)
#todo create method to post to slack/ask alan ?
def post_to_slack(story_array):
    #requests.post()
    print(story_array)

def main():
    try:
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent,
                             username=username,
                             password=password)
        post_print(reddit)

    except prawcore.exceptions.OAuthException:
        print("could not log in ")

    except prawcore.exceptions:
        print("unable to create reddit instance")


if __name__ == '__main__':
    main()
