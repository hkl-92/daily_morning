from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
#START_DATE：2022-02-03
start_date = os.environ['START_DATE']
#城市：深圳、成都
city = os.environ['CITY']
city1 = os.environ['CITY1']
#BIRTHDAY：09-18
birthday = os.environ['BIRTHDAY']
#BIRTHDAY1：12-11
birthday1 = os.environ['BIRTHDAY1']
#START_DARRY：2023-01-09
start_marry = os.environ['START_DARRY']
#MARRY：01-09
marry = os.environ['MARRY']
#测试公众号信息：APP_ID、APP_SECRET
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
#关注公众号用户信息：USER_ID、USER_ID1
user_id = os.environ["USER_ID"]
user_id1 = os.environ["USER_ID1"]
#模板ID：TEMPLATE_ID
template_id = os.environ["TEMPLATE_ID"]

#获取深圳温度、天气
def get_weather():
  # url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  # res = requests.get(url).json()
  # weather = res['data']['list'][0]
  # return weather['weather'], math.floor(weather['temp'])
  url = "http://t.weather.sojson.com/api/weather/city/101280601"
  res = requests.get(url).json()
  # res.encoding='utf-8'
  # resp = res.json()
  # print(res)
  weathers = res['data']
  tem = weathers['wendu'] + '℃'
  # print(tem)
  weather = weathers['forecast'][0]['type']
  # print(weather)
  return weather, tem

#获取成都温度、天气
def get_weather1():
  # url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city1
  # res = requests.get(url).json()
  # weather = res['data']['list'][0]
  # return weather['weather'], math.floor(weather['temp'])
  url = "http://t.weather.sojson.com/api/weather/city/101270101"
  res = requests.get(url).json()
  # res.encoding='utf-8'
  # resp = res.json()
  # print(res)
  weathers = res['data']
  tem = weathers['wendu'] + '℃'
  # print(tem)
  weather = weathers['forecast'][0]['type']
  # print(weather)
  return weather, tem

#获取START_DATE天数
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#获取START_MARRY天数
def get_start_marry():
  delta = today - datetime.strptime(start_marry, "%Y-%m-%d")
  return delta.days

#获取BIRTHDAY距今天数
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#获取BIRTHDAY1距今天数
def get_birthday1():
  next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#获取MARRY距今天数
def get_marry():
  next = datetime.strptime(str(date.today().year) + "-" + marry, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#获取短语
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

#获取字体颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, temperature = get_weather()
wea1, temperature1 = get_weather1()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()},"weather1":{"value":wea1},"temperature1":{"value":temperature1},"birthday_left1":{"value":get_birthday1()},"marry":{"value":get_marry()},"start_marry":{"value":get_start_marry()}}
res = wm.send_template(user_id, template_id, data)
res1 = wm.send_template(user_id1, template_id, data)
print(res)
print(res1)

