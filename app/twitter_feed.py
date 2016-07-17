import twitter
import json

class TwitterFeed:
    TWEET_COUNT = 10

    def __init__(self):
        with open('config.json') as data_source:
            self.config = json.load(data_source)

        self.api = twitter.Api(consumer_key=self.config['consumer_key'],
                               consumer_secret=self.config['consumer_secret'],
                               access_token_key=self.config['access_token_key'],
                               access_token_secret=self.config['access_token_secret'])
        self.__get_timeline__()
        self.__offset = 0

    def __get_timeline__(self):
        self.timeline = dict()

        try:
            statuses = self.api.GetUserTimeline(screen_name='A_single_bear',
                                                exclude_replies=True,
                                                count=200,
                                                page=1)
            self.timeline['tweets'] = [s.text.replace('#', 'hash tag') for s in statuses]
            with open('content/tweets.json', 'w') as outfile:
                json.dump(self.timeline, outfile)
        except:
            """If we have an API failure, load cached tweets"""
            with open('content/tweets.json') as infile:
                self.timeline = json.load(infile)

    def get_tweet(self, index):
        self.current_tweet = self.timeline['tweets'][self.__offset + index]
        return self.current_tweet

    def reset(self):
        self.__offset = 0

    def load_more(self):
        """We already have 200 stories..."""
        """No reason to do another network request."""
        self.__offset += self.TWEET_COUNT
        if self.__offset >= len(self.timeline['tweets']) - self.TWEET_COUNT:
            self.__offset = 0
