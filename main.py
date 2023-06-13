from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
from bs4 import BeautifulSoup
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
city1 = os.environ['CITY1']

birthday = os.environ['BIRTHDAY']
birthday1 = os.environ['BIRTHDAY1']
marry = os.environ['MARRY']
start_marry = os.environ['START_MARRY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id1 = os.environ["USER_ID1"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  # 设置深圳城市编码
  city_code = '101280601'
  # 深圳天气的 url 地址
  url = 'http://www.weather.com.cn/weather1d/{}.shtml'.format(city_code)
  #返回的内容出现乱码，可能是因为中文编码格式不一致所致。这个问题可以通过设置 requests 库的 headers 来解决。
  #在 headers 中添加 accept-encoding 和 user-agent 等参数，防止被反爬虫机制拦截，使请求正常工作。之后再解析页面内容即可正常显示中文。
  # 设置请求头 headers
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Encoding': 'gzip, deflate',
  }
  # 发送请求获取响应
  response = requests.get(url, headers=headers)
  # 使用 BeautifulSoup 解析响应内容
  soup = BeautifulSoup(response.content, 'html.parser')
  # 提取需要的天气信息
  tagToday = soup.find('p', class_="tem")  # 当前温度
  tagWind = soup.find('p', class_="win")  # 风力信息
  tagSoup = soup.find('p', class_="wea")  # 天气信息
  # 输出温度信息
  tem = str(int((tagToday.text)[0:3])) + '℃'
  # 输出天气信息
  weather = tagSoup.text
  # 输出风力信息
  win = tagWind.text
  return weather, tem

def get_weather1():
  # 设置成都城市编码
  city_code = '101270101'
  #构造城市对应的 url 地址
  url = 'http://www.weather.com.cn/weather1d/{}.shtml'.format(city_code)
  # 设置请求头 headers
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Encoding': 'gzip, deflate',
  }
  # 发送请求获取响应
  response = requests.get(url, headers=headers)
  # 使用 BeautifulSoup 解析响应内容
  soup = BeautifulSoup(response.content, 'html.parser')
  # 提取需要的天气信息
  tagToday = soup.find('p', class_="tem")  # 当前温度
  tagWind = soup.find('p', class_="win")  # 风力信息
  tagSoup = soup.find('p', class_="wea")  # 天气信息
  # 输出温度信息
  tem = str(int((tagToday.text)[0:3])) + '℃'
  # 输出天气信息
  weather = tagSoup.text
  # 输出风力信息
  win = tagWind.text
  return weather, tem

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday1():
  next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_marry():
  next = datetime.strptime(str(date.today().year) + "-" + marry, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_start_marry():
  delta = today - datetime.strptime(start_marry, "%Y-%m-%d")
  return delta.days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

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

