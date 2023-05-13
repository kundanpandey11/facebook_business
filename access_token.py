import requests

"""
permission required for hiding comment:

pages_manage_instant_articles
pages_show_list
ads_management
ads_read
business_management
leads_retrieval
pages_read_engagement
pages_manage_metadata
pages_read_user_content
pages_manage_ads
pages_manage_posts
pages_manage_engagement
public_profile


"""
## FOR AD ACCOUNTS
# api keys of graph api APP
# update this in pythonanywhere 
api_key = ""
api_secret = ""

## FOR AD ACCOUNTS
ACCESS_TOKEN = ""
LONGLIVED_ACCESS_TOKEN = ""

## FOR USER ACCESS TOKEN
USER_ACCESS_TOKEN = ""
USER_LONGLIVED_ACCESS_TOKEN = ""

def get_long_lived_access_token():
    url = u"https://graph.facebook.com/v16.0/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(api_key, api_secret, USER_ACCESS_TOKEN)
    access = requests.get(url)
    print(access.content)


# get_long_lived_access_token()