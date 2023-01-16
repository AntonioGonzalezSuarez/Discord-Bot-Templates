import tweepy
from dotenv import load_dotenv
import os
from typing import List, Union

load_dotenv()


def get_client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    api_key=os.getenv("TWITTER_API_KEY"),
    api_secret=os.getenv("TWITTER_API_KEY_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
):
    if (
        api_key is None
        or api_secret is None
        or access_token is None
        or access_token_secret is None
        or bearer_token is None
    ):
        print("Missing twitter tokens to create client")
        raise Exception("Missing authorization to tweet")
    client = tweepy.Client(
        bearer_token, api_key, api_secret, access_token, access_token_secret
    )
    return client


def get_api(
    api_key=os.getenv("TWITTER_API_KEY"),
    api_secret=os.getenv("TWITTER_API_KEY_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
):
    if (
        api_key is None
        or api_secret is None
        or access_token is None
        or access_token_secret is None
    ):
        raise Exception("Missing tokens")
    auth = tweepy.OAuth1UserHandler(
        api_key, api_secret, access_token, access_token_secret
    )
    return tweepy.API(auth)


def send_tweet(tweet_text: str, media_url: str = None, **kwargs):
    client = get_client(**kwargs)
    extra_args = {}
    if media_url is not None:
        api = get_api()
        media = api.media_upload(filename=media_url)
        extra_args["media_ids"] = [media.media_id_string]
    client.create_tweet(text=tweet_text, user_auth=True, **extra_args)
    print("tweet Successful!")


def delete_tweet(id_list: Union[int, List[int]]):
    client = get_client()
    list(map(lambda i: client.delete_tweet(i, user_auth=True), id_list))
    print("Deleted tweet succesful")


def get_client_info():
    client = get_client()
    return client.get_me()


def get_tweets(username=None):
    client = get_client()
    if username is None:
        username = client.get_me().data["username"]
    tweets = client.search_recent_tweets(
        query=f"from:{username}", user_auth=True, tweet_fields=["created_at"]
    ).data
    result = {}
    if tweets is None:
        return result
    for tw in tweets:
        result[tw.id] = {}
        result[tw.id] = {
            "text": tw.text,
            "utc_time_post": tw.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
        }
    return result
