import os
import requests
import smtplib
from dotenv import load_dotenv
import datetime
from datetime import timedelta

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#stocks part
api_key_stocks = os.getenv('api_key_stocks')

parameters_stocks ={'function':'TIME_SERIES_DAILY',
             'symbol':STOCK,
             'apikey':api_key_stocks,
}
response = requests.get(url=STOCK_ENDPOINT,params=parameters_stocks)
data = response.json()
#Dates
today_date = datetime.datetime.today().date()
yesterday = today_date - timedelta(days=1)
before_yesterday = yesterday - timedelta(days=1)
# print(data)
#calculating the difference
day1_close = float(data['Time Series (Daily)'][str(before_yesterday)]['4. close'])
day2_close = float(data['Time Series (Daily)'][str(yesterday)]['4. close'])
difference = ((day2_close - day1_close)/day1_close)*100
stock_up_down = f'🔻{(difference):.2f}%' if difference < 0 else f'🔺{(difference):.2f}%'



#news part
api_key_news = os.getenv('api_key_news')
news_params = {
    'q':'tesla',
    'sortBy':'popularity',
    'from':str(before_yesterday),
    'apiKey':api_key_news,
}
response2 =requests.get(url=NEWS_ENDPOINT,params=news_params)
data2 = response2.json()
article = data2['articles'][0]['source']['name']
title = data2['articles'][0]['title']
description = str(data2['articles'][0]['description'])



body =f"""
   {STOCK} : {stock_up_down}\n
   Headline:  {title}\n
   Brief:  {description}\n
   article:  {article}\n
"""
emails = os.getenv('my_email')
passwords =os.getenv('password')
with smtplib.SMTP('smtp.gmail.com') as connection :
    connection.starttls()
    connection.login(user=emails,password=passwords)
    connection.sendmail(to_addrs='your email',from_addr=emails,msg=f'Subject:Tesla news\n\n{body}')



