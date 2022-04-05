import requests
from bs4 import BeautifulSoup
import re
import tweepy
import numpy as np
import datetime
import os

date_now = datetime.datetime.now()
Consumer_Key = os.environ['Consumer_Key']
Consumer_Secret = os.environ['Consumer_Secret']
Access_Token = os.environ['Access_Token']
Access_Token_Secret = os.environ['Access_Token_Secret']

def jbbf_sc():
    flag = 0
    all_flag = 0
    month_flag = np.load('month_update_data.npy')
    update_month = []
    push_message = ''

    for i in range(1,13):
        if i<10:
            url = "https://www.jbbf.jp/contests/?prefecture_id=12&hold_time_month=20220"+str(i)
        else:
            url = "https://www.jbbf.jp/contests/?prefecture_id=12&hold_time_month=2022"+str(i)

        r = requests.get(url)
        target = BeautifulSoup(r.text, 'html.parser')
        extract = target.find('h3')
        info = re.findall("(ありません)",extract.text)

        if info == ['ありません']:
            flag = 0
        else:
            flag = 1

        if flag != month_flag[i-1]:
            month_flag[i-1] = flag
            all_flag = 1
            update_month.append(i)

    if all_flag == 0:
        push_message = date_now.strftime('%Y年%m月%d日')+"現在、更新はありません。"
    else:
        if update_month[0] < 10:
            site_url = "https://www.jbbf.jp/contests/?prefecture_id=12&hold_time_month=20220"+str(update_month[0])
        else:
            site_url = "https://www.jbbf.jp/contests/?prefecture_id=12&hold_time_month=2022"+str(update_month[0])

        push_message = date_now.strftime('%Y年%m月%d日')+'ホームページに更新がありました！\n確認はこちら\n'+site_url

    np.save('month_update_data.npy', month_flag)
    return push_message

auth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)

api.update_status(jbbf_sc())