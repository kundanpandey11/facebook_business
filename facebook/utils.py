from urllib.request import urlopen
import json 
from textblob import TextBlob
import plotly.offline as opy
import plotly.graph_objs as go
import urllib.request 
from access_token import LONGLIVED_ACCESS_TOKEN, USER_LONGLIVED_ACCESS_TOKEN


import requests 

# LONGLIVED_ACCESS_TOKEN = "EAAHUhP0dyaEBANyRC1owKo0hrqWQiW1JYW7ufRe1KyEWaFwdkSJXPZBXkZAA73G2m8IhrAgOB5TW5ZCdzdkwZCWYNpMcvbLycjbaqFzepZAu6QZA5sMYWAhvZBli7IjzhujgP9FkQrZAYScHb0BadqRDtu5u65OmHXkzWRDq4KQdwUDt8I8NkbB5RjCXNR0DEB6a0d8dPDhjyQZDZD"

# adset name
def get_adset_name(adset_id="6345796776582"):
    adset_url = f"https://graph.facebook.com/v16.0/{adset_id}?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
    adsets = json.loads(urllib.request.urlopen(adset_url).read()) 
    adset_name = adsets['name']
    return adset_name


def get_capaign_name_and_id(account_id="act_296865963"):
    campaign_url = f"https://graph.facebook.com/v16.0/{account_id}/campaigns?effective_status=%5B%22ACTIVE%22%2C%22PAUSED%22%5D&fields=name%2Cobjective&access_token={LONGLIVED_ACCESS_TOKEN}"
    campaigns_json = json.loads(urllib.request.urlopen(campaign_url).read())
    return campaigns_json['data']

def get_single_campaign(campaign_id=6338868866982):
    campaign_url = f"https://graph.facebook.com/v16.0/{campaign_id}?fields=name&access_token={LONGLIVED_ACCESS_TOKEN}"
    campaigns_json = json.loads(urllib.request.urlopen(campaign_url).read())
    print(campaigns_json['name'])
    return campaigns_json['name']

def get_adsets_from_campaign(campaign_id):
    campaign_ads= f"https://graph.facebook.com/v16.0/{campaign_id}/adsets?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
    adsets = json.loads(urllib.request.urlopen(campaign_ads).read()) 
    # add ads count to the same dictionary
    for d in adsets['data']:
        ads_url = f"https://graph.facebook.com/v16.0/{d['id']}/ads?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
        ads = json.loads(urllib.request.urlopen(ads_url).read()) 
        d['ad_count'] = len(ads['data'])
    print(adsets['data'])
    return adsets['data']


def get_ad_id_list(campaign_id = "6338868868582"): # all ads from wholesale as there are comments
    campaign_ads= f"https://graph.facebook.com/v16.0/{campaign_id}/ads?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
    ads_json = json.loads(urllib.request.urlopen(campaign_ads).read())  
    comment_id_list = []
    for d in ads_json['data']:
        comment_id_list.append(d['id'])
    # print(comment_id_list)
    return comment_id_list

def get_ad_name_and_effective_object_story_id(ad_id="6338868872182"):
    ad_url = f"https://graph.facebook.com/v16.0/{ad_id}?fields=id,name,creative.fields(effective_object_story_id),insights.fields(actions)&access_token={LONGLIVED_ACCESS_TOKEN}"
    ad_json = json.loads(urllib.request.urlopen(ad_url).read()) 
    ad_name = ad_json['name']
    effective_object_story_id = ad_json['creative']['effective_object_story_id']
    return ad_name, effective_object_story_id


def get_sentiment_graph(effective_object_story_id="114113634875896_142641242042511", post_title="static", access_token=LONGLIVED_ACCESS_TOKEN):
    ads_comment_url  = f"https://graph.facebook.com/v16.0/{effective_object_story_id}/comments?fields=id,message,is_hidden&summary=true&access_token={access_token}&pretty=1&summary=true&limit=100&after"
    ads_comments_json = json.loads(urllib.request.urlopen(ads_comment_url).read()) 
    # print(len(ads_comments_json['data']))
    comment_and_graph = {}
    comments = []
    comment_list = []
    positive_sentiment = negative_sentiment = neutral_sentiment = 0
    for d in ads_comments_json['data']:
        comment_polarity = TextBlob(d['message']).sentiment.polarity
        comments.append(d['message'])
        status = d['is_hidden']
        if comment_polarity < 0.0:
            negative_sentiment += 1   
            # status = comment_status(d['id'])     
            comment_list.append({"negative_message": d['message'], "id":d['id'], "is_hidden":status})
        elif comment_polarity > 0.0:
            comment_list.append({"positive_message": d['message'], "id":d['id'], "is_hidden":status})
            positive_sentiment += 1
        elif comment_polarity == 0.0:
            comment_list.append({"neutral_message": d['message'], "id":d['id'], "is_hidden":status})
            neutral_sentiment += 1
    value = [negative_sentiment,  positive_sentiment, neutral_sentiment]
    names = ['Negative Comments', 'Positive Comments', 'Neutral Comments']
    comment_and_graph['Comments'] = comment_list
    if sum(value) != 0:  
        trace1 = go.Bar(x=names, y=value )
        data=go.Data([trace1])
        layout=go.Layout(title=post_title, xaxis={'title':'Comments'}, yaxis={'title':'Count'})
        figure=go.Figure(data=data,layout=layout, ) 
        figure.update_traces(marker_color=['red',  'green', 'blue',])             
        div = figure.to_html(
            full_html=False, default_height=400, 
            default_width=500,
            config=dict(displayModeBar=False))
        comment_and_graph['Graph'] = div
        comment_and_graph['adname'] = effective_object_story_id
        return comment_and_graph
    else:
        return "No comments found"

# get total comment count in the ad
# if the comment count is less than 3 then don't build a graph
def comment_count(eff):
    comment_url = f"https://graph.facebook.com/v16.0/{eff}/comments?fields=id,toplevel,message&access_token={LONGLIVED_ACCESS_TOKEN}"
    comment_json = json.loads(urllib.request.urlopen(comment_url).read())
    comment_len = len(comment_json['data'])
    return comment_len

def comment_info(comment_id):
    comment_url = f"https://graph.facebook.com/v16.0/{comment_id}?fields=id,message&access_token={LONGLIVED_ACCESS_TOKEN}"
    comment_json = json.loads(urllib.request.urlopen(comment_url).read())
    return comment_json['message']

# hide and unhide comments
def hide_comment(comment_id):
    url = f"https://graph.facebook.com/v16.0/{comment_id}"
    comment_hide = {
        "is_hidden": "true",
        "access_token":LONGLIVED_ACCESS_TOKEN
        }
    response = requests.post(url, json=comment_hide)
    if response.status_code == 200:
        print('Comment hidden successfully.')
    else:
        print('Error hiding comment:', response.json()['error']['message'])

def unhide_comment(comment_id):
    url = f"https://graph.facebook.com/v16.0/{comment_id}"
    comment_hide = {
        "is_hidden": "false",
        "access_token":LONGLIVED_ACCESS_TOKEN
        }
    response = requests.post(url, json=comment_hide)
    if response.status_code == 200:
        print('Comment revealed successfully.')
    else:
        print('Error hiding comment:', response.json()['error']['message']) 

# check if the comments is hidden 
def comment_status(comment_id):
    url = f"https://graph.facebook.com/v16.0/{comment_id}?fields=is_hidden,can_hide&access_token={LONGLIVED_ACCESS_TOKEN}"
    status = json.loads(urllib.request.urlopen(url).read()) 
    return status["is_hidden"]

#<<=======================================================================================================================>>
#FACEBOOK ACCOUNT SECTION LOGIC 

def get_account_name(page_id, page_access_token):
    url = f"https://graph.facebook.com/v16.0/{page_id}?fields=id,name&access_token={page_access_token}"
    read_url = json.loads(urllib.request.urlopen(url).read())
    return read_url["name"]


def get_account_post_list(account_id, account_access_token):
    url = f"https://graph.facebook.com/v16.0/{account_id}/posts?fileds=id,message&access_token={account_access_token}&limit=30"
    read_url = json.loads(urllib.request.urlopen(url).read())
    post_id = []
    for a in read_url['data'][:20]:
        post_id.append(a['id'])
    # print(post_id)
    return post_id


def get_post_photos(post_id,page_access_token):
    url = f"https://graph.facebook.com/v16.0/{post_id}?fields=id,full_picture&access_token={page_access_token}"
    # print(url)
    read_url = json.loads(urllib.request.urlopen(url).read())
    full_picture = read_url['full_picture']
    return full_picture


def get_post_comment_count(post_id, account_access_token):
    url = f"https://graph.facebook.com/v16.0/{post_id}/comments?summary=true&access_token={account_access_token}&limit=10"
    read_url = json.loads(urllib.request.urlopen(url).read())
    comment_count = read_url['summary']['total_count']
    # print(comment_count)
    return comment_count



#<<===========================================================================================================================>>
# previous logic for facebook post comments 
def get_post_name_from_commentid(commentid, account_data):
    comment_id = split_id(commentid, 0)
    for d in account_data:
        d_id = split_id(d['id'], 1)
        if d_id == comment_id:
            post_name = d['message']
            # return d_id 
    if d_id:
        return post_name
    else:
        return "NO Post name available"
        
def split_id(string, index):
    id = string.split("_")[index]
    return id


def get_account_name(acc_id, access_token):
    account_url =  u"https://graph.facebook.com/{0}?access_token={1}".format(
                        acc_id,
                        access_token,)
    account_info = json.loads(urlopen(account_url).read())
    # print(account_info)
    return account_info['name']