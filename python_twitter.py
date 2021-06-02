import twitter
from collections import Counter

api = twitter.Api(consumer_key="sxIAQ8hCXS49yhvipGdamK2FP",
                  consumer_secret="BjWAdmEmKrwxq6Q21mF32sF1ZzaMxx6Zl71pDzvtA1Tz9g0yNJ",
                  access_token_key="1399192492440911877-PYLYgo4pGui4VqtknhvzbGbMdfe7VG",
                  access_token_secret="BMov3etkNVcp0XwuapSEvPWPMGyLe6FDfUBJsKpOlW0Yq")

account = "@elonmusk"
statuses = api.GetUserTimeline(screen_name=account, count=200, include_rts=True, exclude_replies=False)

#for status in statuses:
#    print(status.text)
result = []

query = "#BTC"
statuses = api.GetSearch(term=query, count=1000)
#print(statuses)
for status in statuses:
    for tag in status.hashtags:
        result.append(tag.text)

print(Counter(result).most_common())
