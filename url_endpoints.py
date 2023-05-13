from urllib.request import urlopen
from textblob import TextBlob
import json 
from decouple import config
import requests
import urllib
import time
import requests
import plotly.offline as opy
import plotly.graph_objs as go
from access_token import USER_LONGLIVED_ACCESS_TOKEN, LONGLIVED_ACCESS_TOKEN, api_key,api_secret, ACCESS_TOKEN







# api_key = config('GEORGE_APP_ID')
# api_secret = config('GEORGE_APP_SCRET')


def get_long_lived_access_token():
    url = u"https://graph.facebook.com/v16.0/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(api_key, api_secret, ACCESS_TOKEN)
    access = requests.get(url)
    print(access.content)




# @shared_task
def get_all_leads():
    ads_id = "723940182548849"
    # all_leads = f""
    all_leads = f"https://graph.facebook.com/{ads_id}/leads?access_token={LONGLIVED_ACCESS_TOKEN}"
    leads_object = json.loads(urllib.request.urlopen(all_leads).read())
    print(leads_object)
    json_object = json.dumps(leads_object)
    json_file = open('JSON/data.json', 'w', encoding='utf-8')
    json_file.write(json_object)
    json_file.close()    
    store_email_to_json()                    
    
def intersection(test_list, remove_list):
    res = [i for i in test_list if i not in remove_list]
    return res


def store_email_to_json(file_path="JSON/data.json"):
    email_dir = {}
    email_list = []
    with open(file_path, 'r', encoding='utf-8') as json_file:
        file_data = json.load(json_file)
    print(len(file_data['data']))
    for d in file_data['data']:
        for n in d['field_data']:
            if n['name'] == 'email':
                # print(n['values'])
                email = n['values']
                email_list.extend(email)
    print(len(email_list))
    email_dir["email"] = email_list # store the email from the current leads 
    old_email_json = open("JSON/emails.json", "r+", encoding='utf-8') # read the existing email.json
    old_email_data = json.load(old_email_json)
    new_email = intersection(email_dir['email'], old_email_data['email'])
    print(new_email)
    print(len(new_email))
    email_dir['new_email'] = new_email


    # create new email section 
    # email_json = open("JSON/emails.json", 'w', encoding='utf-8')
    # email_data = json.
    # old_email_data['new_email'] = new_email
    # json.dumps(old_email_json)
    # old_email_json.close()

    email_json = open('JSON/emails.json', 'w', encoding='utf-8')
    json_obejct = json.dumps(email_dir, indent=4)
    email_json.write(json_obejct)
    email_json.close()


def secondsToDays(seconds):
    day  =  60 * 60 * 24
    days = seconds / day
    days = round(days)
    print(days)

# get_long_lived_access_token()
# store_email_to_json()


# need to be filtered for every hour of the day and get 100 emails posible
def full_url():
    ads_id = "723940182548849"
    all_leads = f"https://graph.facebook.com/{ads_id}/leads?access_token={LONGLIVED_ACCESS_TOKEN}"
    print(all_leads)

    

def get_unique_email_and_send_email():
    email_file = open('JSON/dummy_email.json', 'r', encoding='utf-8')
    email_data = json.load(email_file)
    print(email_data['email'])

# store_email_to_json()

def get_ads_posts():
    ads_id = "723940182548849"
    business_id=191432099114844

    # all_leads = f""
    all_leads = f"https://graph.facebook.com/v16.0/{business_id}/owned_ad_accounts?access_token={LONGLIVED_ACCESS_TOKEN}"
    leads_object = json.loads(urllib.request.urlopen(all_leads).read())
    print(leads_object)                 



# works 
def get_all_campaigns():
    # get all the campaign from smart solutio business account.
    all_campaign = f"https://graph.facebook.com/v16.0/act_296865963/campaigns?effective_status=%5B%22ACTIVE%22%2C%22PAUSED%22%5D&fields=name%2Cobjective&access_token={LONGLIVED_ACCESS_TOKEN}"
    campaign_object = json.loads(urllib.request.urlopen(all_campaign).read()) 
    print(campaign_object)
    print(all_campaign)


def get_campaign_ads(campaign_id=6338868866982): # campaign id of kapunga rice retail kenya
    campaign_ads= f"https://graph.facebook.com/v16.0/{campaign_id}/ads?fields=id,name,insights&access_token={LONGLIVED_ACCESS_TOKEN}"
    campaign_object = json.loads(urllib.request.urlopen(campaign_ads).read()) 
    print(campaign_object)
    print(campaign_ads)


def get_campaign_adsets(campaign_id=6338868866982): # campaign id of kapungs rice retail kenya
    campaign_ads= f"https://graph.facebook.com/v16.0/{campaign_id}/adsets?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
    campaign_object = json.loads(urllib.request.urlopen(campaign_ads).read()) 
    print(campaign_object)
    print(campaign_ads)



def get_ad_comments(ad_id):
    ad_comment_url = f"https://graph.facebook.com/v16.0/{ad_id}?fields=creative.fields(effective_object_story_id),insights.fields(actions)&access_token={LONGLIVED_ACCESS_TOKEN}"
    print(ad_comment_url)
    commnet_x_id = "114113634875896_169411869365448"
    more_url = f"https://graph.facebook.com/v16.0/{commnet_x_id}/comment?summary=true&access_token={LONGLIVED_ACCESS_TOKEN}"
    print(more_url)


def get_capaign_name_and_id(account_id="act_296865963"):

    campaign_url = f"https://graph.facebook.com/v16.0/{account_id}/campaigns?effective_status=%5B%22ACTIVE%22%2C%22PAUSED%22%5D&fields=name%2Cobjective&access_token={LONGLIVED_ACCESS_TOKEN}"
    campaigns_json = json.loads(urllib.request.urlopen(campaign_url).read())

    return campaigns_json['data']

    
def get_single_campaign(campaign_id=6338868866982):
    campaign_url = f"https://graph.facebook.com/v16.0/{campaign_id}?fields=name&access_token={LONGLIVED_ACCESS_TOKEN}"
    campaigns_json = json.loads(urllib.request.urlopen(campaign_url).read())
    print(campaigns_json['name'])
    return campaigns_json['name']



def get_ad_id_list(campaign_id = 6338868868582): # all ads from wholesale as there are comments
    campaign_ads= f"https://graph.facebook.com/v16.0/{campaign_id}/ads?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
    ads_json = json.loads(urllib.request.urlopen(campaign_ads).read())  
    comment_id_list = []
    for d in ads_json['data']:
        comment_id_list.append(d['id'])
    print(comment_id_list)
    return comment_id_list




def get_sentiment_graph(effective_object_story_id="114113634875896_142641242042511", post_title="static"):
    ads_comment_url  = f"https://graph.facebook.com/v16.0/{effective_object_story_id}/comments?summary=true&access_token={LONGLIVED_ACCESS_TOKEN}&pretty=1&summary=true&limit=100&after"
    ads_comments_json = json.loads(urllib.request.urlopen(ads_comment_url).read()) 
    print(len(ads_comments_json['data']))
    comment_and_graph = {}
    comments = []
    # negative_comment_and_id = {}
    negative_comment_list = []
    positive_sentiment = negative_sentiment = neutral_sentiment = 0
    for d in ads_comments_json['data']:
        comment_polarity = TextBlob(d['message']).sentiment.polarity
        comments.append(d['message'])
        if comment_polarity < 0.0:
            negative_sentiment += 1
            
            negative_comment_list.append({"negative_message": d['message'], "id":d['id']})
        elif comment_polarity > 0.0:
            negative_comment_list.append({"positive_message": d['message'], "id":d['id']})

            positive_sentiment += 1
        elif comment_polarity == 0.0:
            negative_comment_list.append({"neutral_message": d['message'], "id":d['id']})

            neutral_sentiment += 1
    value = [negative_sentiment, neutral_sentiment, positive_sentiment]
    names = ['Negative Comments', 'Neutral Comments', 'Positive Comments']
    comment_and_graph['Comments'] = negative_comment_list
    if sum(value) != 0:  
        trace1 = go.Bar(x=names, y=value )
        data=go.Data([trace1])
        layout=go.Layout(title=post_title, xaxis={'title':'Comments'}, yaxis={'title':'Count'})
        figure=go.Figure(data=data,layout=layout, ) 
        figure.update_traces(marker_color=['red', 'blue', 'green'])             
        div = figure.to_html(
            full_html=False, default_height=400, 
            default_width=500,
            config=dict(displayModeBar=False))
        comment_and_graph['Graph'] = div
        return comment_and_graph
    else:
        return "No comments found"
    print(negative_comment_list)


# def test_hide_comment(comment_id):
#     url =f"https://graph.facebook.com/v16.0/{comment_id}&access_token={LONGLIVED_ACCESS_TOKEN}&is_hidden=true"
#     requests.post(url)
#     print(url)


# test_hide_comment(comment_id="")

# if the comment count is less than 3 then don't build a graph
def comment_count(eff):
    comment_url = f"https://graph.facebook.com/v16.0/{eff}/comments?fields=id,toplevel,message,is_hidden=true&access_token={LONGLIVED_ACCESS_TOKEN}"
    comment_json = json.loads(urllib.request.urlopen(comment_url).read())
    print(comment_json)
    print(len(comment_json['data']))
    print(comment_url)

    return len(comment_json)
    

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

# comment_count(eff="114113634875896_142641242042511")

def comment_status(comment_id):
    url = f"https://graph.facebook.com/v16.0/{comment_id}?fields=is_hidden,can_hide&access_token={LONGLIVED_ACCESS_TOKEN}"
    status = json.loads(urllib.request.urlopen(url).read()) 
    print(status)
    # print(status['is_hidden'])
    return status["is_hidden"]

# hide_comment(comment_id="132172819756020_3370942606512361")
# time.sleep(5)
# get_ad_id_list()


def get_hidden_comments(eff="114113634875896_142641242042511"):
    url = f"https://graph.facebook.com/v16.0/{eff}/comments?fields=id,toplevel,message&is_hidden=true&access_token={LONGLIVED_ACCESS_TOKEN}&limit=100"
    read_url = json.loads(urllib.request.urlopen(url).read())
    print(read_url)
    print(url)

# unhide_comment("142641242042511_205943025413598") # static 2 cbd comment test
# comment_status("142641242042511_205943025413598")

def get_campaign_id_from_comment(comment_id):
    url = f"https://graph.facebook.com/v16.0/{comment_id}/campaign?fields=id&access_token={LONGLIVED_ACCESS_TOKEN}"
    print(url)


# get_campaign_id_from_comment(comment_id="142641242042511_598652445490857")
# get_hidden_comments()


def get_adsets_from_campaign(campaign_id=6338868866982):
    campaign_ads= f"https://graph.facebook.com/v16.0/{campaign_id}/adsets?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
    adsets = json.loads(urllib.request.urlopen(campaign_ads).read()) 
    
    # add ads count to the same dictionary
    for d in adsets['data']:
        ads_url = f"https://graph.facebook.com/v16.0/{d['id']}/ads?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
        ads = json.loads(urllib.request.urlopen(ads_url).read()) 
        d['ad_count'] = len(ads['data'])
    print(adsets['data'])
    return adsets['data']


def get_adset(adset_id="6345796776582"):
    adset_url = f"https://graph.facebook.com/v16.0/{adset_id}?fields=id,name&access_token={LONGLIVED_ACCESS_TOKEN}"
    adsets = json.loads(urllib.request.urlopen(adset_url).read()) 
    # print(adsets)
    adset_name = adsets['name']
    return adset_name


def comment_info(comment_id):
    comment_url = f"https://graph.facebook.com/v16.0/{comment_id}?fields=id,message&access_token={LONGLIVED_ACCESS_TOKEN}"
    comment_json = json.loads(urllib.request.urlopen(comment_url).read())
    print(comment_json['message'])
    return comment_json['message']

def comments_with_status(eff_id):
    ads_comment_url  = f"https://graph.facebook.com/v16.0/{eff_id}/comments?fields=id,message,is_hidden&summary=true&access_token={LONGLIVED_ACCESS_TOKEN}&pretty=1&summary=true&limit=100&after"
    ads_json = json.loads(urllib.request.urlopen(ads_comment_url).read())
    print(ads_json)
    print(ads_comment_url)


ads_comment_url  = f"https://graph.facebook.com/v16.0/114113634875896_142641242042511/comments?fields=id,message,is_hidden&summary=true&access_token={LONGLIVED_ACCESS_TOKEN}&pretty=1&summary=true&limit=100&after"
ads_comments_json = json.loads(urllib.request.urlopen(ads_comment_url).read()) 
# print(ads_comments_json)





# GER Wholesale: 114113634875896
def get_post_comments(post_id):
    post_url = f"https://graph.facebook.com/v16.0/{post_id}/comments?summary=true&access_token=EAAHUhP0dyaEBAEsPyCMzP7Vn7MmL2RcjlkBmYFUSAJM7R0FUgDZARZCKDDSaoDLyQN1rMb0Ma0BF756TIEM51no58xVUr4BKFuQZBc0fSX06sZBXPXsWSZCcAPyItN1IJOEsQUea3ukBOYwvShZC3WPoAEFUptua0CvVoLUE7tdVBEvSDoYzeWNzPLL35tsnbpCACLFeAvGQZDZD&pretty=1&summary=true&limit=100&after"
    print(post_url)

# get_account_post_list(account_id="114113634875896")
# get_post_comments(1)

"""
GER Wholesale: 
114113634875896 : 
EAAHUhP0dyaEBAJLvmrZCK7PcF4VefIjHUEsHrJtcookJWdEi3FVqJIodu6FyLetZAI67gA60hkikBCKtqZCqwC2j0mZB57ZC6NZBS1lIIlgjkhgOAsfZB2sePV1dZCT2xqcS7e8UHSJ2SprBEEijw5gCtngwj8evEUm8k0eshlLTDIKhbaOMmiReNE5giwuyOy8QSPJbbCd1uQZDZD
"""

def get_account_name(page_id, page_access_token):
    url = f"https://graph.facebook.com/v16.0/{page_id}?fields=id,name&access_token={page_access_token}"
    read_url = json.loads(urllib.request.urlopen(url).read())
    return read_url["name"]

# get_account_name("108165061108164", "EAAHUhP0dyaEBACQzYUPL2eh0Go855dcC4QPCNWORq1zZBqWSzHZCSXEgfUGNKztCQtiIbDRGqD9ziPCPJ7mjAVji9I2ltKAtgj2fnYZBqistWZCZBtjimZA7oSrqDPOfJR2zXPzcHPWmrCOTbzCNaqeZCBYcni1kCSRU9ivIcDGF0ZCzO8trnaeIgrNo0ADLEFE1vCKcRDnrjgZDZD")



def get_account_post_list(account_id, account_access_token):
    url = f"https://graph.facebook.com/v16.0/{account_id}/posts?fileds=id,message&access_token={account_access_token}&limit=30"
    read_url = json.loads(urllib.request.urlopen(url).read())
    post_id = []
    for a in read_url['data'][:20]:
        post_id.append(a['id'])
    print(post_id)
    return post_id


# get_account_post_list(
#     account_id="114113634875896",
#     account_access_token="EAAHUhP0dyaEBAAI8E1uBPWnXAPlvteQbzTXRQhXGXZBmUAaUO6r2ZCZCFnabMPCVZBSUZCrWsAeLn11QI6FllCChi5RMOYDgOr50OlZC44ZA5TeahwuPPPIq0MmJlDjgIgE8X96m7ogHyZBC71jjck5ahEJX2Px6ksmu7vlN5GAS5ldRecqJ5fhOZBwfnqQ0fhz4zPoe5QYmgfwZDZD")


# get_post_photos("108691721397409_454130653539004", 
#                 "EAAHUhP0dyaEBACQzYUPL2eh0Go855dcC4QPCNWORq1zZBqWSzHZCSXEgfUGNKztCQtiIbDRGqD9ziPCPJ7mjAVji9I2ltKAtgj2fnYZBqistWZCZBtjimZA7oSrqDPOfJR2zXPzcHPWmrCOTbzCNaqeZCBYcni1kCSRU9ivIcDGF0ZCzO8trnaeIgrNo0ADLEFE1vCKcRDnrjgZDZD")

def get_post_comment_count(post_id, account_access_token):
    url = f"https://graph.facebook.com/v16.0/{post_id}/comments?summary=true&access_token={account_access_token}&limit=10"
    read_url = json.loads(urllib.request.urlopen(url).read())
    comment_count = read_url['summary']['total_count']
    # print(comment_count)
    return comment_count


# get_post_comment_count(
#     "114113634875896_177413171898651",
#     "EAAHUhP0dyaEBAAI8E1uBPWnXAPlvteQbzTXRQhXGXZBmUAaUO6r2ZCZCFnabMPCVZBSUZCrWsAeLn11QI6FllCChi5RMOYDgOr50OlZC44ZA5TeahwuPPPIq0MmJlDjgIgE8X96m7ogHyZBC71jjck5ahEJX2Px6ksmu7vlN5GAS5ldRecqJ5fhOZBwfnqQ0fhz4zPoe5QYmgfwZDZD"
# )

def get_post_photos(
        post_id="114113634875896_177413171898651", 
        page_access_token="EAAHUhP0dyaEBAAI8E1uBPWnXAPlvteQbzTXRQhXGXZBmUAaUO6r2ZCZCFnabMPCVZBSUZCrWsAeLn11QI6FllCChi5RMOYDgOr50OlZC44ZA5TeahwuPPPIq0MmJlDjgIgE8X96m7ogHyZBC71jjck5ahEJX2Px6ksmu7vlN5GAS5ldRecqJ5fhOZBwfnqQ0fhz4zPoe5QYmgfwZDZD"):
    url = f"https://graph.facebook.com/v16.0/{post_id}?fields=id,full_picture&access_token={page_access_token}"
    # print(url)
    read_url = json.loads(urllib.request.urlopen(url).read())

    full_picture = read_url['full_picture']
    print(full_picture)

get_post_photos()