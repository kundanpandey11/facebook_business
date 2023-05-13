from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from urllib.request import urlopen
import time 
from textblob import TextBlob
import urllib.request 
import json
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import requests 
# from social_django.apps.django_app.default.models import UserSocialAuth

import plotly.offline as opy
import plotly.graph_objs as go

from .utils import (
    get_sentiment_graph, get_ad_id_list, 
    get_ad_name_and_effective_object_story_id, 
    get_capaign_name_and_id, get_adsets_from_campaign,
    get_single_campaign, comment_count, comment_status,
    hide_comment, comment_info, get_adset_name, LONGLIVED_ACCESS_TOKEN
    )





def sentiment_graph(request, adset_id):
    all_campaigns = get_capaign_name_and_id()

    try:
        graph_container = []
        ad_id_list = get_ad_id_list(campaign_id=adset_id)
        adset_name = get_adset_name(adset_id=adset_id)

        for ad_id in ad_id_list:
            name, eff = get_ad_name_and_effective_object_story_id(ad_id=ad_id)
            comment_len = comment_count(eff)
            if comment_len > 2:
                graph = get_sentiment_graph(effective_object_story_id=eff, post_title=name)
                graph_container.append(graph)
        context = {
            "graph_container":graph_container,
            "all_campaigns":all_campaigns,
            "adset_name":adset_name,
            "adset_id":adset_id, 
        }
        return render(request, "sentiment-graph.html", context)
    except Exception as e:
        print(e)
        return render(request, "404NOADS.html", {"all_campaigns":all_campaigns})


# get list of adsets from the campains and also display the campaing name
def adset_list(request, campaign_id):
    adsets = get_adsets_from_campaign(campaign_id=campaign_id)
    campaign_name = get_single_campaign(campaign_id=campaign_id)
    all_campaigns = get_capaign_name_and_id()
    context = {
        "adsets":adsets,
        "all_campaigns":all_campaigns,
        "campaign_name":campaign_name
    }
    return render(request, "adset_list.html", context)




def Hide_comment(request, adset_id, comment_id):
    url = f'https://graph.facebook.com/{comment_id}'
    data = {
        'is_hidden': 'true',
        'access_token': LONGLIVED_ACCESS_TOKEN
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        comment_message = comment_info(comment_id)
        messages.success(
            request, 
            "Your request was successful. \nComment : `{}` is hidden now from users.".format(comment_message)
            )
    else:
        print(response.text)
        messages.error(request, "Request Failed! {}".format(response.text))
    return HttpResponseRedirect(reverse('sentiment-graph', kwargs={'adset_id': adset_id}))


def Unhide_comment(request, adset_id, comment_id):
    url = f'https://graph.facebook.com/{comment_id}'
    data = {
        'is_hidden': 'false',
        'access_token': LONGLIVED_ACCESS_TOKEN
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        comment_message = comment_info(comment_id)
        messages.success(
            request, 
            "Your request was successful. \nComment : `{}` is unhidden now from users.".format(comment_message)
            )
    else:
        print(response.text)
        messages.error(request, "Request Failed! {}".format(response.text))
    return HttpResponseRedirect(reverse('sentiment-graph', kwargs={'adset_id': adset_id}))