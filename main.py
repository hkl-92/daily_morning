#coding=UTF-8

from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
from bs4 import BeautifulSoup
import os
import random
from zhdate import ZhDate          # 农历 ↔ 公历

today = datetime.now()
#在一起
start_date = os.environ['START_DATE']
#城市 深圳、成都
city = os.environ['CITY']
city1 = os.environ['CITY1']
#生日
birthday = os.environ['BIRTHDAY']
birthday1 = os.environ['BIRTHDAY1']
#结婚纪恋日
marry = os.environ['MARRY']
#结婚后
start_marry = os.environ['START_MARRY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id1 = os.environ["USER_ID1"]
template_id = os.environ["TEMPLATE_ID"]

#获取深圳天气
def get_weather():
  # 设置深圳城市编码
  city_code = '101280601'
  keys = 'bc7bec9e1c2e40d9acf46d91303db73a'
  # 深圳天气的 url 地址 原：devapi.qweather.com
  url = 'https://nq7p3xbpph.re.qweatherapi.com/v7/weather/now?location={}&key={}'.format(city_code, keys)
  # 返回的内容出现乱码，可能是因为中文编码格式不一致所致。这个问题可以通过设置 requests 库的 headers 来解决。
  # 在 headers 中添加 accept-encoding 和 user-agent 等参数，防止被反爬虫机制拦截，使请求正常工作。之后再解析页面内容即可正常显示中文。
  # 设置请求头 headers
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Encoding': 'gzip, deflate',
  }
  # 发送请求获取响应
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    # 解析JSON响应
    weather_data = response.json()
    # 提取所需数据

    temperature = weather_data['now']['temp']
    condition = weather_data['now']['text']
    Wind = weather_data['now']['windSpeed']
    # 输出温度信息
    # tem = str(int(temperature)) + '℃'
    tem = temperature + '℃'
    # 输出天气信息
    weather = condition
    # 输出风力信息
    win = Wind

  else:
    print("无法获取天气数据")

  return weather, tem

#获取成都天气
def get_weather1():
  # 设置成都城市编码
  city_code = '101270101'
  keys = 'bc7bec9e1c2e40d9acf46d91303db73a'
  # 成都天气的 url 地址 原：devapi.qweather.com
  url = 'https://nq7p3xbpph.re.qweatherapi.com/v7/weather/now?location={}&key={}'.format(city_code, keys)
  # 返回的内容出现乱码，可能是因为中文编码格式不一致所致。这个问题可以通过设置 requests 库的 headers 来解决。
  # 在 headers 中添加 accept-encoding 和 user-agent 等参数，防止被反爬虫机制拦截，使请求正常工作。之后再解析页面内容即可正常显示中文。
  # 设置请求头 headers
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Encoding': 'gzip, deflate',
  }
  # 发送请求获取响应
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    # 解析JSON响应
    weather_data = response.json()
    # 提取所需数据

    temperature = weather_data['now']['temp']
    condition = weather_data['now']['text']
    Wind = weather_data['now']['windSpeed']
    # 输出温度信息
    # tem = str(int(temperature)) + '℃'
    tem = temperature + '℃'
    # 输出天气信息
    weather = condition
    # 输出风力信息
    win = Wind

  else:
    print("无法获取天气数据")

  return weather, tem

#距离当前天数
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#距离你生日天数
# def get_birthday():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days
def get_birthday():
    today = date.today()
    current_year = today.year

    # 解析农历生日字符串
    lunar_month, lunar_day = map(int, birthday.split('-'))

    # 创建当前年的农历生日对象
    try:
      # 首先尝试非闰月
      lunar_birthday = ZhDate(current_year, lunar_month, lunar_day)
    except ValueError:
      # 如果失败，尝试闰月（用负号表示闰月）
      lunar_birthday = ZhDate(current_year, -lunar_month, lunar_day)

    # 转换为公历日期
    next_birthday = lunar_birthday.to_datetime().date()

    # 如果今年的生日已经过去，计算明年的生日
    if next_birthday < today:
      try:
        lunar_birthday_next = ZhDate(current_year + 1, lunar_month, lunar_day)
        next_birthday = lunar_birthday_next.to_datetime().date()
      except ValueError:
        lunar_birthday_next = ZhDate(current_year + 1, -lunar_month, lunar_day)
        next_birthday = lunar_birthday_next.to_datetime().date()

    # 计算天数差
    return (next_birthday - today).days

#距离我生日天数
# def get_birthday1():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days
def get_birthday1():
  today = date.today()
  current_year = today.year

  # 解析农历生日字符串
  lunar_month, lunar_day = map(int, birthday1.split('-'))

  # 创建当前年的农历生日对象
  try:
    # 首先尝试非闰月
    lunar_birthday = ZhDate(current_year, lunar_month, lunar_day)
  except ValueError:
    # 如果失败，尝试闰月（用负号表示闰月）
    lunar_birthday = ZhDate(current_year, -lunar_month, lunar_day)

  # 转换为公历日期
  next_birthday = lunar_birthday.to_datetime().date()

  # 如果今年的生日已经过去，计算明年的生日
  if next_birthday < today:
    try:
      lunar_birthday_next = ZhDate(current_year + 1, lunar_month, lunar_day)
      next_birthday = lunar_birthday_next.to_datetime().date()
    except ValueError:
      lunar_birthday_next = ZhDate(current_year + 1, -lunar_month, lunar_day)
      next_birthday = lunar_birthday_next.to_datetime().date()

  # 计算天数差
  return (next_birthday - today).days

#结婚后天数
def get_start_marry():
  delta = today - datetime.strptime(start_marry, "%Y-%m-%d")
  return delta.days

#结婚纪恋日天数
def get_marry():
  next = datetime.strptime(str(date.today().year) + "-" + marry, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#获取随机文字信息
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

#字体颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

#模版数据填充
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
wea1, temperature1 = get_weather1()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()},
        "weather1":{"value":wea1},"temperature1":{"value":temperature1},"birthday_left1":{"value":get_birthday1()},
        "marry":{"value":get_marry()},"start_marry":{"value":get_start_marry()}}
res = wm.send_template(user_id, template_id, data)
res1 = wm.send_template(user_id1, template_id, data)
print(res)
print(res1)

