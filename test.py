#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time
import random
import threading
import win32gui
import re
import SendKeys
import os

url_login = "http://www.roboocap.net/index.php?route=account/login"
url_cart = "http://www.roboocap.net/index.php?route=checkout/cart"
url_model_room = "http://www.roboocap.net/index.php?route=model/room"

browser = webdriver.Chrome()
browser.maximize_window()

browser.get(url_login)
time.sleep(3) # 等待页面加载完成

# 登录
while True:
	try:
		browser.find_element_by_name("username").clear() # 清空用户名输入框，防止浏览器自动填充
		browser.find_element_by_name("username").send_keys(u"琉璃")
		browser.find_element_by_name("password").send_keys("forget@1t")
		browser.find_element_by_id("text_login").click()
		browser.set_page_load_timeout(60) # 1分钟内未登录成功即为超时
		browser.switch_to.default_content # 跳转到图纸室
		break
	except TimeoutException:
		print "啊哦，超时了！即将重试……"
		time.sleep(2)

# 检测URL是否已经发生变化
while True:
	if browser.current_url != url_login:
		break # 说明已成功跳转到图纸室
	time.sleep(1) # 否则等待1秒

browser.get("http://www.roboocap.net/index.php?route=model/info&mid=1988")
browser.find_element_by_xpath('//a[@href="javascript:add2Cart()"]').click()
time.sleep(1)
browser.find_element_by_id("add2Cart").click()
time.sleep(5)
print browser.find_element_by_xpath('//div[@class="cart-info"]').text == u"该图纸不可以重复加入购物车"
browser.quit()
