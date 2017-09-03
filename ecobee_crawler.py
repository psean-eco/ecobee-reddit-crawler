import praw
import prawcore.exceptions
import reddit_constants
import requests

client_id = reddit_constants.client_id
client_secret = reddit_constants.client_secret
username = reddit_constants.username
password = reddit_constants.password
user_agent = reddit_constants.user_agent
webhook_url = reddit_constants.webhook

def post_print(reddit):
    arr =[]
    title = "Heading:{heading}"
    upvotes = "Upvotes:{votes}"
    comments = "Comments:{comments}"
    link = "Link to Thread:{link} "
    posts = reddit.subreddit('ecobee').new(limit=10)
    for submission in posts:
        story={}
        story["title"] = submission.title
        story ["upvotes"] = submission.ups
        story["link"] = "https://www.reddit.com"+ submission.permalink
        story ["totalComments"] = submission.num_comments
        arr.append(story)
        post_to_slack(story)
    print(arr)


def post_to_slack(story):
    payload={}
    link_text = "<{}| Read More>".format(story['link'])
    payload['txt'] = "--------------------"+"\n"+"_"+ ":triangular_flag_on_post: "+ story['title'] + "_" + " " +" " + link_text  + "\n" +  "Upvotes: {}".format(story['upvotes'])
    response = requests.post(
        webhook_url, json=payload,
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error: {} with error code: {code}'.format(response.text,code=response.status_code)
        )


def main():
    try:
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent,
                             username=username,
                             password=password)
        post_print(reddit)

    except prawcore.exceptions.OAuthException as e :
        print("could not log in because: " + str(e))

    except prawcore.exceptions.ResponseException as e:
        print("unable to create reddit instance because:" + str(e))



if __name__ == '__main__':
    main()
