#!/usr/bin/python
# -*- coding: utf-8 -*-
## 查看生产进度

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

ISOTIMEFORMAT='%Y-%m-%d %X'

browser = webdriver.Chrome()
browser.maximize_window() # 最大化浏览器

url = "http://www.roboocap.net/index.php?route=account/login"
browser.get(url)
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
	if browser.current_url != url:
		break # 说明已成功跳转到图纸室
	time.sleep(1) # 否则等待1秒

f = open("C:\\Users\\Administrator\\Desktop\\learn_python\\Selenium1\\check_production_schedule.txt",'a')
f.write(time.strftime(ISOTIMEFORMAT,time.localtime()))
f.write(u''.join(u"\t查看生产进度").encode('utf-8'))
f.write(u''.join(u"\t账号：琉璃").encode('utf-8'))
f.write('\n\n')

browser.get("http://www.roboocap.net/index.php?route=order/list&status=4")
num_status_4 = int(browser.find_element_by_xpath('//span[@class="num-orders bold"]').text[:2].rstrip())
info = u''.join(u"待生产").encode('utf-8')
f.write(info)
f.write('\n\n')

if num_status_4 > 0:
	for i in range(num_status_4):
		xpath = '//li[' + str(i+1) + ']/div[@class="stream-box"]/div[@class="box-shipment"]/div[@class="grid-inner selfclear"]\
		/div[@class="right-grid"]/a[@class="button-static"][1]'
		browser.find_element_by_xpath(xpath).click()
		time.sleep(3)
		
		element = browser.find_element_by_xpath('//div[@class="selfclear popover"]/p').text
		string = u''.join(element).encode('utf-8').strip()
		f.write(string)
		f.write('\n\n')
		browser.back()
		time.sleep(3)
else:
	f.write(u''.join(u"没有待生产的图纸").encode('utf-8'))
	f.write('\n==========\n\n')

browser.get("http://www.roboocap.net/index.php?route=order/list&status=5")
num_status_5 = int(browser.find_element_by_xpath('//span[@class="num-orders bold"]').text[:2].rstrip())
info = u''.join(u"正在生产").encode('utf-8')
f.write(info)
f.write('\n\n')

if num_status_5 > 0:
	for i in range(num_status_5):
		xpath = '//li[' + str(i+1) + ']/div[@class="stream-box"]/div[@class="box-shipment"]/div[@class="grid-inner selfclear"]\
		/div[@class="right-grid"]/a[@class="button-static"][1]'
		browser.find_element_by_xpath(xpath).click()
		time.sleep(3)
		
		element = browser.find_element_by_xpath('//div[@class="selfclear popover"]/p').text
		string = u''.join(element).encode('utf-8').strip()
		f.write(string)
		f.write('\n\n')
		browser.back()
		time.sleep(3)
else:
	f.write(u''.join(u"没有正在生产的图纸").encode('utf-8'))
	f.write('\n==========\n\n')

f.write('\n')
f.close()
browser.quit()