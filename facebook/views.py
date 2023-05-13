from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from urllib.request import urlopen
import time 
from textblob import TextBlob
import urllib.request 
import json
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import requests 
import plotly.offline as opy
import plotly.graph_objs as go
from access_token import USER_LONGLIVED_ACCESS_TOKEN

from .utils import (
    get_account_name, get_account_post_list,
    get_sentiment_graph, get_post_comment_count,
    get_post_photos, comment_info
)



def get_accounts(request):
    url = f"https://graph.facebook.com/v16.0/me/accounts?access_token={USER_LONGLIVED_ACCESS_TOKEN}"
    accounts_json = json.loads(urllib.request.urlopen(url).read())
    accounts = accounts_json['data']
    # for a in accounts:
        # print(f"{a['name']}: {a['id']} : {a['access_token']}\n")
    context = {
        "accounts":accounts
    }

    return render(request, "facebook_accounts/facebook_accounts.html", context)



def sentiment_graph_posts(request, account_id, account_access_token):
    post_id_list = get_account_post_list(account_id=account_id, account_access_token=account_access_token)
    account_name = get_account_name(acc_id=account_id, access_token=account_access_token)
    graph_container = []
    for post_id in post_id_list:
        comment_count = get_post_comment_count(post_id, account_access_token)
        if comment_count > 0:
            graph = get_sentiment_graph(effective_object_story_id=post_id, access_token=account_access_token, post_title="No Title Available" )
            try:
                picture_url = get_post_photos(post_id=post_id, page_access_token=account_access_token)
            except Exception as e:
                # print(e)
                picture_url = ""
            graph['full_picture_url'] = picture_url
            graph['access_token'] = account_access_token
            graph_container.append(graph)
    context = {
                "graph_container":graph_container,
                "adset_name":account_name,
                "adset_id":account_id, 
            }
    return render(request, "facebook_accounts/sentiment_graph.html", context)



def Post_hide_comment(request, account_id, comment_id, account_access_token):
    url = f'https://graph.facebook.com/{comment_id}'
    data = {
        'is_hidden': 'true',
        'access_token': account_access_token
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        comment_message = comment_info(comment_id)
        messages.success(
            request, 
            "Your request was successful. \nComment : `{}` is hidden now from users.".format(comment_message)
            )
    else:
        # print(response.text)
        messages.error(request, "Request Failed! {}".format(response.text))
    return HttpResponseRedirect(
        reverse('sentiment-graph-post', 
        kwargs={'account_id': account_id, "account_access_token":account_access_token}))


def Post_unhide_comment(request, account_id, comment_id, account_access_token):
    url = f'https://graph.facebook.com/{comment_id}'
    data = {
        'is_hidden': 'false',
        'access_token': account_access_token
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        comment_message = comment_info(comment_id)
        messages.success(
            request, 
            "Your request was successful. \nComment : `{}` is unhidden now from users.".format(comment_message)
            )
    else:
        # print(response.text)
        messages.error(request, "Request Failed! {}".format(response.text))
    return HttpResponseRedirect(
        reverse('sentiment-graph-post', 
        kwargs={'account_id': account_id, "account_access_token":account_access_token}))