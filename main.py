import requests
import os
from twilio.rest import Client

STOCK = "TCS"
COMPANY_NAME = "Tata Consultancy Services"

STOCK_PRICE_API_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILLIO_SID = os.getenv("twillio_sid")

STOCK_PRICE_API_KEY = os.getenv("stock_price_api_key")
NEWS_API_KEY = os.getenv("news_api_key")
TWILLIO_AUTH_TOKEN = os.getenv("twillio_auth_token")
TWILLIO_VERIFIED_PHONE_NO = os.getenv("twillio_verified_phone_no")
TWILLIO_VIRTUAL_PHONE_NO = os.getenv("twillio_virtual_phone_no")

stock_price_parameters = {
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":"TCS.BSE",
    "apikey":STOCK_PRICE_API_KEY
}

response = requests.get(url=STOCK_PRICE_API_ENDPOINT, params=stock_price_parameters)
stock_price_data = response.json()["Time Series (Daily)"]
stock_price_data_list = [value for (key, value) in stock_price_data.items()]
yesterday_closing_price = stock_price_data_list[0]["4. close"]
day_before_yesterday_closing_price = stock_price_data_list[1]["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 5:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference/float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 5:
    news_parameters={
        "apiKey":NEWS_API_KEY,
        "qInTitle":COMPANY_NAME
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILLIO_SID, TWILLIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="TWILLIO_VERIFIED_PHONE_NO",
            to="TWILLIO_VERIFIED_PHONE_NO"
        )


